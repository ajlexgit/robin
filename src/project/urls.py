from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from main import views as main_views
from .sitemaps import site_sitemaps


urlpatterns = [
    url(r'^$', main_views.IndexView.as_view(), name='index'),
    url(r'^forms/$', main_views.FormsView.as_view(), name='forms'),
    url(r'^404/$', 'django.views.defaults.page_not_found'),
    url(r'^500/$', 'django.views.defaults.server_error'),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^robokassa/', include('robokassa.urls', namespace='robokassa')),

    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    url(r'^dladmin/comments/', include('comments.admin_urls', namespace='admin_comments')),
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
