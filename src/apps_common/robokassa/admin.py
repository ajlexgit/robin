from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars
from project.admin import ModelAdminMixin
from .models import Log


@admin.register(Log)
class LogAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'step', 'status', 'message', 'created',
            ),
        }),
    )
    list_filter = ('status',)
    list_display = ('step', 'status', 'short_message', 'created')
    readonly_fields = ('step', 'status', 'message', 'created')
    list_display_links = ('step', 'short_message', )
    date_hierarchy = 'created'

    def short_message(self, obj):
        return truncatechars(obj.message, 48)
    short_message.short_description = _('Message')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
