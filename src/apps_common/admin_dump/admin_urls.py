from django.conf.urls import patterns, url
from . import admin_views


urlpatterns = patterns('',
    url(r'^index/$', admin_views.index, name='index'),
    url(r'^create/$', admin_views.make_dump, name='create'),
)
