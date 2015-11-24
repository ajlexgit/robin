from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from project.admin import ModelAdminMixin
from .models import SampleBlock


@admin.register(SampleBlock)
class SampleBlockAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('label', 'visible'),
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('title',),
        }),
    )
    list_display = ('label', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
    )
