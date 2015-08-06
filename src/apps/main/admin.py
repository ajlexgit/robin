from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from comments.admin import CommentsModelAdminMixin
from attachable_blocks import AttachableBlockRefTabularInline
from .models import MainPageConfig, MainBlockFirst, MainBlockSecond, InlineSample


class InlineSampleAdmin(admin.TabularInline):
    model = InlineSample
    extra = 0
    suit_classes = 'suit-tab suit-tab-header'


class MyPageBlockRefInline(AttachableBlockRefTabularInline):
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(MainBlockFirst)
class MainBlockFirstAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')


@admin.register(MainBlockSecond)
class MainBlockSecondAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'visible')


@admin.register(MainPageConfig)
class MainPageConfigAdmin(CommentsModelAdminMixin, SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-header'),
            'fields': ('header_title', 'preview', 'text', 'description', 'color', 'color2' ,'price', 'gallery'),
        }),
    )
    inlines = (InlineSampleAdmin, MyPageBlockRefInline)
    suit_form_tabs = (
        ('header', _('Header')),
        ('comments', _('Comments')),
        ('blocks', _('Blocks')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'
    suit_comments_position = 'bottom'
    suit_comments_tab = 'comments'
