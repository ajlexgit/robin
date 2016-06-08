from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from project.admin import ModelAdminMixin
from .models import SocialPost


@admin.register(SocialPost)
class SocialPostAdmin(ModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'network', 'text', 'url', 'image',
            ),
        }),
    )
    list_display = ('network_icon', '__str__', 'url', 'created')
    list_display_links = ('network_icon', '__str__')
    list_filter = ('network', )
    suit_form_tabs = (
        ('general', _('General')),
    )

    def network_icon(self, obj):
        return """<img src="">"""
    network_icon.short_description = _('#')
    network_icon.allow_tags = True
