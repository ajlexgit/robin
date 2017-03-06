from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from admin_honeypot.admin import honeypot_site
from main import views as main_views
from .sitemaps import site_sitemaps


urlpatterns = [
    url(r'^admin/', include(honeypot_site.urls)),
    url(r'^dladmin/social/', include('social_networks.admin_urls', namespace='admin_social_networks')),
    url(r'^dladmin/autocomplete/', include('libs.autocomplete.urls', namespace='autocomplete')),
    url(r'^dladmin/ckeditor/', include('ckeditor.admin_urls', namespace='admin_ckeditor')),
    url(r'^dladmin/gallery/', include('gallery.admin_urls', namespace='admin_gallery')),
    url(r'^dladmin/users/', include('users.admin_urls', namespace='admin_users')),
    url(r'^dladmin/ctr/', include('admin_ctr.urls', namespace='admin_ctr')),
    url(r'^dladmin/', include(admin.site.urls)),

    url(r'^$', main_views.IndexView.as_view(), name='index'),
    url(r'^404/$', 'django.views.defaults.page_not_found'),
    url(r'^500/$', 'django.views.defaults.server_error'),
    url(r'^away/$', 'libs.away.views.away', name='away'),
    url(r'^jsi18n/$', 'project.views.cached_javascript_catalog', name='jsi18n'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': site_sitemaps}),

    url(r'^ckeditor/', include('ckeditor.urls', namespace='ckeditor')),
    url(r'^blocks/', include('attachable_blocks.urls', namespace='blocks')),
    url(r'^placeholder/', include('placeholder.urls', namespace='placeholder')),
    url(r'^social/', include('social_networks.urls', namespace='social_networks')),

    url(r'^contact/', include('contacts.urls', namespace='contacts')),
]


if settings.DEBUG:
    urlpatterns += [
        # Для доступа к MEDIA-файлам при разработке
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            kwargs={'document_root': settings.MEDIA_ROOT}
        ),
        url(
            r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            kwargs={'document_root': settings.STATIC_ROOT}
        ),
    ]
