from django.conf.urls import patterns, url
from . import admin_views


urlpatterns = patterns('',
    url(r'^index/$', admin_views.index, name='index'),
    url(r'^create/$', admin_views.create, name='create'),
    url(r'^delete/(?P<filename>\w+)/$', admin_views.delete, name='delete'),
    url(r'^download/(?P<filename>\w+)/$', admin_views.download, name='download'),
)
