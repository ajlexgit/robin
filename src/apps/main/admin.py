from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from comments.admin import CommentsModelAdminMixin
from .models import MainPageConfig, InlineSample


class InlineSampleAdmin(admin.TabularInline):
    model = InlineSample
    extra = 0
    suit_classes = 'suit-tab suit-tab-header'


@admin.register(MainPageConfig)
class MainPageConfigAdmin(CommentsModelAdminMixin, SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-header'),
            'fields': ('header_title', 'preview', 'text', 'description', 'color'),
        }),
    )
    inlines = (InlineSampleAdmin, )
    suit_form_tabs = (
        ('header', _('Header')),
        ('comments', _('Comments')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'
    suit_comments_position = 'bottom'
    suit_comments_tab = 'comments'
