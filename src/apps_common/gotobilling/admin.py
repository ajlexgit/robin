from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars
from project.admin import ModelAdminMixin
from .models import Log


@admin.register(Log)
class LogAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'status', 'message', 'request', 'created',
            ),
        }),
    )
    list_filter = ('inv_id', 'status')
    list_display = ('status', 'short_message', 'created')
    readonly_fields = ('status', 'message', 'request', 'created')
    list_display_links = ('short_message', )
    date_hierarchy = 'created'

    def suit_row_attributes(self, obj, request):
        css_class = {
            Log.STATUS_SUCCESS: 'success',
            Log.STATUS_ERROR: 'error',
        }.get(obj.status)
        if css_class:
            return {'class': css_class}

    def short_message(self, obj):
        return truncatechars(obj.message, 48)
    short_message.short_description = _('Message')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
