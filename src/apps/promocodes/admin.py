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
            'parameter': forms.TextInput({
                'class': 'input-small'
            })
        }

    class Media:
        css = {
            'all': (
                'promocodes/admin/css/promocode.css',
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        strategy_name = cleaned_data.get('strategy_name', '')
        return STRATEGIES[strategy_name].validate(self, cleaned_data)


@admin.register(PromoCode)
class PromoCodeAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'code', 'strategy_name', 'parameter',
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
    list_display = ('code', 'strategy_format', 'times_used', 'redemption_limit_format', 'start_date', 'end_date')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def strategy_format(self, obj):
        return obj.strategy.full_description(obj)
    strategy_format.admin_order_field = 'strategy'
    strategy_format.short_description = _('Strategy')

    def times_used(self, obj):
        return obj.usages.count()
    times_used.short_description = _('Times Used')

    def redemption_limit_format(self, obj):
        if obj.redemption_limit:
            return obj.redemption_limit
        else:
            return _('Unlimited')
    redemption_limit_format.admin_order_field = 'redemption_limit'
    redemption_limit_format.short_description = _('Redemption limit')

