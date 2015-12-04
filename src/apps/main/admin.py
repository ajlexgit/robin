from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from seo.admin import SeoModelAdminMixin
from attachable_blocks import AttachedBlocksTabularInline
from .models import MainPageConfig


class BlocksInline(AttachedBlocksTabularInline):
    suit_classes = 'suit-tab suit-tab-blocks'


@admin.register(MainPageConfig)
class MainPageConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'preview',
            ),
        }),
    )
    inlines = (BlocksInline, )
    suit_form_tabs = (
        ('general', _('General')),
        ('blocks', _('Blocks')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'

