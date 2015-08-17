from django.conf.urls import patterns, url
from . import admin_views


urlpatterns = patterns('',
    url(r'^create/$', admin_views.create, name='create'),
    url(r'^delete/$', admin_views.delete, name='delete'),
    url(r'^upload/$', admin_views.upload, name='upload'),
    url(r'^upload_video/$', admin_views.upload_video, name='upload_video'),
    url(r'^sort/$', admin_views.sort, name='sort'),
    url(r'^delete_item/$', admin_views.delete_item, name='delete_item'),
    url(r'^rotate_item/$', admin_views.rotate_item, name='rotate_item'),
    url(r'^crop_item/$', admin_views.crop_item, name='crop_item'),
    url(r'^get_description/$', admin_views.get_description, name='get_description'),
    url(r'^set_description/$', admin_views.set_description, name='set_description'),
)
