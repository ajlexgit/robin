from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from attachable_blocks import AttachedBlocksTabularInline
from seo.admin import SeoModelAdminMixin
from .models import ContactsConfig, MessageReciever


class BlocksInline(AttachedBlocksTabularInline):
    suit_classes = 'suit-tab suit-tab-blocks'


class MessageRecieverAdmin(admin.TabularInline):
    model = MessageReciever
    extra = 0
    min_num = 1
    suit_classes = 'suit-tab suit-tab-messages'


@admin.register(ContactsConfig)
class ContactsConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'title',
            ),
        }),
    )
    inlines = (MessageRecieverAdmin, BlocksInline)
    suit_form_tabs = (
        ('general', _('General')),
        ('messages', _('Messages')),
        ('blocks', _('Blocks')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'
