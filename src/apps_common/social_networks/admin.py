from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage
from project.admin import ModelAdminMixin
from .models import SocialPost
from . import conf

SPRITE_ICONS = (
    conf.NETWORK_TWITTER,
    conf.NETWORK_FACEBOOK,
    conf.NETWORK_GOOGLE,
    'linkedin',
    'pinterest',
    'youtube',
    'instagram',
)


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
    list_filter = ('network', 'created')
    search_fields = ('text',)
    suit_form_tabs = (
        ('general', _('General')),
    )

    def suit_cell_attributes(self, obj, column):
        """ Классы для ячеек списка """
        default = super().suit_cell_attributes(obj, column)
        if column == 'network_icon':
            default.setdefault('class', '')
            default['class'] += ' mini-column'
        return default

    def network_icon(self, obj):
        icons_url = staticfiles_storage.url('social_networks/img/admin_icons.svg')
        try:
            icon_code, icon_title = next((
                network_tuple
                for network_tuple in conf.NETWORKS
                if network_tuple[0] == obj.network
            ))
        except StopIteration:
            return

        offset = 100 / (len(SPRITE_ICONS) - 1) * SPRITE_ICONS.index(icon_code)
        return """
        <span style="display:inline-block; width:21px; height:20px; margin:0;
        background:url(%s) %0.4f%% 0; vertical-align:middle;" title="%s"/>""" % (
            icons_url, offset, icon_title
        )
    network_icon.short_description = _('#')
    network_icon.allow_tags = True
