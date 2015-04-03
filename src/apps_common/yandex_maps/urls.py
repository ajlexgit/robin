from django.conf.urls import patterns, url
from . import views_ajax


urlpatterns = patterns('',
    url(r'^get_coords/$', views_ajax.get_coords, name='get_coords'),
)
