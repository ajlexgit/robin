from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import IndexView
from .sitemaps import site_sitemaps


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^404/$', 'django.views.defaults.page_not_found'),
    url(r'^500/$', 'django.views.defaults.server_error'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^langs/', include('multilanguage.urls', namespace='multilanguage')),

    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    url(r'^dladmin/comments/', include('comments.admin_urls', namespace='admin_comments')),
    url(r'^dladmin/gallery/', include('gallery.admin_urls', namespace='admin_gallery')),
    url(r'^dladmin/users/', include('users.admin_urls', namespace='admin_users')),
    url(r'^dladmin/dump/', include('admin_dump.admin_urls', namespace='admin_dump')),
    url(r'^dladmin/', include(admin.site.urls)),

    url(r'^jsi18n/$', 'project.views.cached_javascript_catalog', name='jsi18n'),
    url(r'^away/$', 'libs.away.views.away', name='away'),
    url(r'^autocomplete/', include('libs.autocomplete.urls', namespace='autocomplete')),
    url(r'^ckeditor/', include('libs.ckeditor.urls', namespace='ckeditor')),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': site_sitemaps}),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        # Для доступа к MEDIA-файлам при разработке
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            kwargs={'document_root': settings.MEDIA_ROOT}
        ),
    )
