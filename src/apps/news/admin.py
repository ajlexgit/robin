from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from attachable_blocks import AttachedBlocksTabularInline
from seo.admin import SeoModelAdminMixin
from .models import NewsPageConfig, Post


class NewsPageBlocksInline(AttachedBlocksTabularInline):
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(NewsPageConfig)
class NewsPageConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
    inlines = (NewsPageBlocksInline, )
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'


@admin.register(Post)
class PostAdmin(SeoModelAdminMixin, ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title', 'slug', 'text', 'is_visible',
            ),
        }),
    )
    inlines = (NewsPageBlocksInline,)
    search_fields = ('title', )
    list_display = ('view', '__str__', 'is_visible')
    list_display_links = ('__str__', )
    actions = ('action_hide', 'action_show')
    prepopulated_fields = {
        'slug': ('title', ),
    }
    suit_form_tabs = (
        ('general', _('General')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

    def action_hide(self, request, queryset):
        queryset.update(is_visible=False)
    action_hide.short_description = _('Hide selected %(verbose_name_plural)s')

    def action_show(self, request, queryset):
        queryset.update(is_visible=True)
    action_show.short_description = _('Show selected %(verbose_name_plural)s')
