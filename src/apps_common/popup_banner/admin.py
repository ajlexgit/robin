from django import forms
from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.utils.translation import ugettext_lazy as _
from project.admin.base import ModelAdminMixin, ModelAdminInlineMixin
from .models import Banner, PageAttachment


class PageAttachmentInline(ModelAdminInlineMixin, TabularInline):
    model = PageAttachment
    extra = 0
    min_num = 1
    suit_classes = 'suit-tab suit-tab-pages'


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'

    def clean(self):
        since_date = self.cleaned_data.get('since_date')
        to_date = self.cleaned_data.get('to_date')

        if to_date is not None and to_date < since_date:
            self.add_error('to_date', "'to_date' should not be less than 'since_date'")

        return self.cleaned_data


@admin.register(Banner)
class BannerAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'label', 'url',
            ),
        }),
        (_('Content'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'image', 'header', 'text', 'button_text',
            ),
        }),
        
        (None, {
            'classes': ('suit-tab', 'suit-tab-opts'),
            'fields': (
                'timeout', 'show_type', 'is_visible', 'since_date', 'to_date', 
            ),
        }),
    )
    form = BannerForm
    list_display = ('__str__', 'url', 'timeout', 'show_type', 'since_date', 'to_date')
    inlines = (PageAttachmentInline,)
    suit_form_tabs = (
        ('general', _('General')),
        ('opts', _('Options')),
    )

    suit_form_includes = (
        ('popup_banner/admin/help_include.html', 'bottom', 'opts'),
    )
