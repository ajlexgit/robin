from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from .models import MainPageConfig, InlineSample


class InlineSampleAdmin(admin.TabularInline):
    model = InlineSample
    extra = 0


@admin.register(MainPageConfig)
class MainPageConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-header'),
            'fields': ('header_title', 'preview', 'text', 'description', 'color'),
        }),
    )
    inlines = (InlineSampleAdmin, )
    suit_form_tabs = (
        ('header', _('Header')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'