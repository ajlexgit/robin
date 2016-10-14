from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from project.admin.base import ModelAdminMixin
from .models import PromoCode
from .strategies import STRATEGIES


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = '__all__'
        widgets = {
            'code': forms.TextInput({
                'class': 'input-large'
            }),
            'parameter': forms.TextInput({
                'class': 'input-small'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        strategy_name = cleaned_data.get('strategy_name', '')
        return STRATEGIES[strategy_name].validate_form(self, cleaned_data)


@admin.register(PromoCode)
class PromoCodeAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'code',
            ),
        }),
        (_('Action'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'strategy_name', 'parameter',
            ),
        }),
        (_('Limits'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'redemption_limit', 'start_date', 'end_date',
            ),
        }),
    )
    form = PromoCodeForm
    list_display = (
        '__str__', 'code', 'strategy_format', 'times_used', 'redemption_limit_format', 'start_date', 'end_date'
    )
    list_display_links = ('__str__', 'code')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def strategy_format(self, obj):
        strategy = STRATEGIES.get(obj.strategy_name)
        return strategy.full_description(obj) if strategy else None
    strategy_format.admin_order_field = 'strategy'
    strategy_format.short_description = _('Strategy')

    def times_used(self, obj):
        return obj.times_used
    times_used.short_description = _('Times Used')

    def redemption_limit_format(self, obj):
        if obj.redemption_limit:
            return obj.redemption_limit
        else:
            return _('Unlimited')
    redemption_limit_format.admin_order_field = 'redemption_limit'
    redemption_limit_format.short_description = _('Redemption limit')

