from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(
        r'^result/$',
        views.result,
        name='result'
    ),
    url(
        r'^success/$',
        views.success,
        name='success'
    ),
    url(
        r'^fail/$',
        views.fail,
        name='fail'
    ),
)
