from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from main import views as main_views
from .sitemaps import site_sitemaps


urlpatterns = [
    url(r'^$', main_views.IndexView.as_view(), name='index'),
    url(r'^404/$', 'django.views.defaults.page_not_found'),
    url(r'^500/$', 'django.views.defaults.server_error'),
    url(r'^blocks/', include('attachable_blocks.urls', namespace='blocks')),
    url(r'^sitemap/', include('sitemap.urls', namespace='sitemap')),

    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^contacts/', include('contacts.urls', namespace='contacts')),
    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    url(r'^dladmin/gallery/', include('gallery.admin_urls', namespace='admin_gallery')),
    url(r'^dladmin/users/', include('users.admin_urls', namespace='admin_users')),
    url(r'^dladmin/dump/', include('admin_dump.admin_urls', namespace='admin_dump')),
    url(r'^dladmin/', include(admin.site.urls)),

    url(r'^jsi18n/$', 'project.views.cached_javascript_catalog', name='jsi18n'),
    url(r'^away/$', 'libs.away.views.away', name='away'),
    url(r'^autocomplete/', include('libs.autocomplete.urls', namespace='autocomplete')),
    url(r'^ckeditor/', include('ckeditor.urls', namespace='ckeditor')),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': site_sitemaps}),
]


if settings.DEBUG:
    urlpatterns += [
        # Для доступа к MEDIA-файлам при разработке
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            kwargs={'document_root': settings.MEDIA_ROOT}
        ),
    ]
