import re
from html import unescape
from django.contrib import admin
from django.conf.urls import url
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.http.response import Http404, JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage
from project.admin import ModelAdminMixin
from .models import SocialPost
from .forms import SocialPostForm, AutpostForm
from . import conf

re_newlines = re.compile(r'\n[\s\n]+')
AUTOPOST_FORM_PREFIX = 'autopost'
SPRITE_ICONS = (
    conf.NETWORK_TWITTER,
    conf.NETWORK_FACEBOOK,
    conf.NETWORK_GOOGLE,
    conf.NETWORK_LINKEDIN,
    'pinterest',
    'instagram',
)


@admin.register(SocialPost)
class SocialPostAdmin(ModelAdminMixin, admin.ModelAdmin):
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

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

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


class AutoPostMixin(ModelAdminMixin):
    change_form_template = 'social_networks/admin/change_form.html'

    class Media:
        js = (
            'social_networks/admin/js/autopost.js',
        )
        css = {
            'all': (
                'social_networks/admin/css/autopost.css',
            )
        }

    def has_autopost_permissions(self, request):
        """ Проверка, есть ли права на редактирование автопостинга """
        return request.user.has_perm('social_networks.change_socialpost')

    def get_autopost_text(self, obj):
        raise NotImplementedError

    def get_autopost_url(self, obj):
        return obj.get_absolute_url()

    def get_autopost_form(self, request, obj):
        initial_text = self.get_autopost_text(obj)
        initial_text = unescape(strip_tags(initial_text)).strip()
        initial_text = re_newlines.sub('\n', initial_text)
        initial_text = initial_text[:conf.TEXT_MAX_LENGTH]

        if request.method == 'POST':
            return AutpostForm(
                request.POST,
                request.FILES,
                initial={
                    'text': initial_text,
                },
                prefix=AUTOPOST_FORM_PREFIX
            )
        else:
            return AutpostForm(
                initial={
                    'text': initial_text,
                },
                prefix=AUTOPOST_FORM_PREFIX
            )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if not add:
            info = self.model._meta.app_label, self.model._meta.model_name
            context.update({
                'has_share_permission': self.has_autopost_permissions(request),
                'share_form': self.get_autopost_form(request, obj),
                'share_form_url': reverse('admin:%s_%s_share' % info, args=(obj.pk,)),
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_urls(self):
        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name
        submit_urls = [
            url(r'^(\d+)/share/$', self.admin_site.admin_view(self.submit_view), name='%s_%s_share' % info),
        ]
        return submit_urls + urls

    def submit_view(self, request, object_id):
        try:
            obj = self.model._default_manager.get(pk=object_id)
        except self.model.DoesNotExist:
            raise Http404

        form = self.get_autopost_form(request, obj)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            networks = form.cleaned_data.get('networks')
            for network in networks:
                SocialPost.objects.create(
                    network=network,
                    url=request.build_absolute_uri(self.get_autopost_url(obj)),
                    text=text,
                )

            return JsonResponse({})
        else:
            return JsonResponse({
                'errors': form.errors
            }, status=400)
