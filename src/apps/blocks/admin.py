from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import MyBlock


@admin.register(MyBlock)
class MyBlockAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('label', 'visible'),
        }),
        (_('Private'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ('title',),
        }),
    )
    list_display = ('label', 'visible')
    suit_form_tabs = (
        ('general', _('General')),
    )
