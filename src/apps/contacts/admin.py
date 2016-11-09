from django.conf import settings
from django.contrib import admin
from django.utils import dateformat
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin
from suit.admin import SortableModelAdmin, SortableTabularInline
from project.admin import ModelAdminMixin, ModelAdminInlineMixin
from attachable_blocks import AttachedBlocksStackedInline
from seo.admin import SeoModelAdminMixin
from libs.description import description
from .models import ContactsConfig, Address, PhoneNumber, NotificationReceiver, ContactBlock, Message


class ContactsConfigBlocksInline(AttachedBlocksStackedInline):
    """ Подключаемые блоки """
    suit_classes = 'suit-tab suit-tab-blocks'


class NotificationReceiverAdmin(ModelAdminInlineMixin, admin.TabularInline):
    """ Получатели сообщений """
    model = NotificationReceiver
    extra = 0
    min_num = 1
    suit_classes = 'suit-tab suit-tab-notify'


@admin.register(ContactsConfig)
class ContactsConfigAdmin(SeoModelAdminMixin, SingletonModelAdmin):
    """ Главная страница """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'header',
            ),
        }),
    )
    inlines = (NotificationReceiverAdmin, ContactsConfigBlocksInline)
    suit_form_tabs = (
        ('general', _('General')),
        ('notify', _('Notifications')),
        ('blocks', _('Blocks')),
    )


class PhoneNumberAdmin(ModelAdminInlineMixin, SortableTabularInline):
    model = PhoneNumber
    extra = 0
    sortable = 'sort_order'
    suit_classes = 'suit-tab suit-tab-phones'


@admin.register(Address)
class AddressAdmin(ModelAdminMixin, SortableModelAdmin):
    """ Адрес """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('address', 'city', 'region', 'zip', 'coords'),
        }),
    )
    list_display = ('city', 'address',)
    sortable = 'sort_order'
    inlines = (PhoneNumberAdmin,)
    suit_form_tabs = (
        ('general', _('General')),
        ('phones', _('Phones')),
    )

    class Media:
        js = (
            'contacts/admin/js/coords.js',
        )


@admin.register(Message)
class MessageAdmin(ModelAdminMixin, admin.ModelAdmin):
    """ Сообщение """
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('name', 'phone', 'email', ),
        }),
        (_('Text'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('message', ),
        }),
        (_('Info'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('date_fmt', 'referer'),
        }),
    )
    readonly_fields = ('name', 'phone', 'email', 'message', 'date_fmt', 'referer')
    list_display = ('name', 'message_fmt', 'date_fmt')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

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
        (_('Customization'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('header',),
        }),
    )
    list_display = ('label', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
    )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
