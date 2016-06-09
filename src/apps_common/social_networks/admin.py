from django import forms
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
    conf.NETWORK_LINKEDIN,
    'pinterest',
    'instagram',
)


class SocialPostForm(forms.ModelForm):
    network = forms.ChoiceField(
        required=True,
        choices=conf.ALLOWED_NETWORKS,
        initial=SocialPost._meta.get_field('network').default,
        label=SocialPost._meta.get_field('network').verbose_name.capitalize(),
    )

    class Meta:
        model = SocialPost
        fields = '__all__'




@admin.register(SocialPost)
class SocialPostAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_list_template = 'social_networks/admin/rss_list.html'

    fieldsets = (
        (None, {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'network', 'url', 'text', 'scheduled',
            ),
        }),
        (_('Dates'), {
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': (
                'created', 'posted'
            ),
        }),
    )
    form = SocialPostForm
    list_display = ('network_icon', '__str__', 'scheduled', 'created', 'posted')
    list_display_links = ('network_icon', '__str__')
    list_filter = ('network', 'created')
    readonly_fields = ('created', 'posted')
    actions = ('action_schedule_posts', 'action_unschedule_posts')
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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            networks=conf.ALLOWED_NETWORKS,
        )
        return super().changelist_view(request, extra_context)

    def network_icon(self, obj):
        icons_url = staticfiles_storage.url('social_networks/img/admin_icons.svg')
        try:
            icon_code, icon_title = next((
                network_tuple
                for network_tuple in conf.ALL_NETWORKS
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

    def action_schedule_posts(self, request, queryset):
        queryset.update(scheduled=True)
    action_schedule_posts.short_description = _('Schedule %(verbose_name_plural)s to be published')

    def action_unschedule_posts(self, request, queryset):
        queryset.update(scheduled=False)
    action_unschedule_posts.short_description = _('Unschedule %(verbose_name_plural)s to be published')
