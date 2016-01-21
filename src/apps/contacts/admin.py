from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from project.admin import ModelAdminMixin
from attachable_blocks import AttachedBlocksStackedInline
from seo.admin import SeoModelAdminMixin
from libs.description import description
from .models import ContactsConfig, MessageReciever, ContactBlock, Message


class ContactsConfigBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


class MessageRecieverAdmin(admin.TabularInline):
    """ Инлайн получалей сообщений """
    model = MessageReciever
    extra = 0
    min_num = 1
    suit_classes = 'suit-tab suit-tab-messages'


@admin.register(ContactsConfig)
class ContactsConfigAdmin(SeoModelAdminMixin, ModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
    inlines = (MessageRecieverAdmin, ContactsConfigBlocksInline)
    suit_form_tabs = (
        ('general', _('General')),
        ('messages', _('Messages')),
        ('blocks', _('Blocks')),
        ('seo', _('SEO')),
    )
    suit_seo_tab = 'seo'


@admin.register(Message)
class MessageAdmin(ModelAdminMixin, admin.ModelAdmin):
    """ Сообщение """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('name', 'phone', 'email', 'date_fmt'),
        }),
        (_('Text'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('message',),
        }),
    )
    readonly_fields = ('date_fmt',)
    list_display = ('user', 'message_fmt', 'date_fmt')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def has_add_permission(self, request):
        return False

    def user(self, obj):
        return str(obj)
    user.short_description = _('User')
    user.admin_order_field = 'name'

    def message_fmt(self, obj):
        return description(obj.message, 60, 80)
    message_fmt.short_description = _('Message')
    message_fmt.admin_order_field = 'message'

    def date_fmt(self, obj):
        return dateformat.format(localtime(obj.date), settings.DATETIME_FORMAT)
    date_fmt.short_description = _('Date')
    date_fmt.admin_order_field = 'date'


@admin.register(ContactBlock)
class ContactBlockAdmin(ModelAdminMixin, admin.ModelAdmin):
    """ Подключаемый блок с контактной формой """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('label', 'visible'),
        }),
        (_('Customize'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('header',),
        }),
    )
    list_display = ('label', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
    )
