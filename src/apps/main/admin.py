from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from .models import MainPageConfig


class MainPageConfigForm(forms.ModelForm):
    class Meta:
        model = MainPageConfig
        widgets = {
            'header_title': forms.TextInput(attrs={
                'class': 'input-xxlarge',
            }),
        }


@admin.register(MainPageConfig)
class MainPageConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    form = MainPageConfigForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-header'),
            'fields': ('header_title', 'address', 'coords', 'coords2'),
        }),
    )
    suit_form_tabs = (
        ('header', _('Header')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

    def __init__(self, *args, **kwargs):
        super().__init__(*args,  **kwargs)
        self.ADDITION_JS += (
            'main/admin/js/main.js',
        )