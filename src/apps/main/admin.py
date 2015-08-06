from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from comments.admin import CommentsModelAdminMixin
from attachable_blocks import AttachableBlockRefTabularInline
from .models import MainPageConfig, MainBlockFirst, MainBlockSecond, MainPageBlockRef, InlineSample


class InlineSampleAdmin(admin.TabularInline):
    model = InlineSample
    extra = 0
    suit_classes = 'suit-tab suit-tab-header'


@admin.register(MainBlockFirst)
class MainBlockFirstAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')


@admin.register(MainBlockSecond)
class MainBlockSecondAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')


class MainPageBlockRefInline(AttachableBlockRefTabularInline):
    model = MainPageBlockRef
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(MainPageConfig)
class MainPageConfigAdmin(CommentsModelAdminMixin, SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-header'),
            'fields': ('header_title', 'preview', 'text', 'description', 'color', 'color2' ,'price', 'gallery'),
        }),
    )
    inlines = (InlineSampleAdmin, MainPageBlockRefInline)
    suit_form_tabs = (
        ('header', _('Header')),
        ('comments', _('Comments')),
        ('blocks', _('Blocks')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'
    suit_comments_position = 'bottom'
    suit_comments_tab = 'comments'
