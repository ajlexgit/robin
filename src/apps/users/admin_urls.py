from django.conf.urls import patterns, url
from . import admin_views


urlpatterns = patterns('',
    url(r'^login_as/(?P<user_id>\d+)/$', admin_views.login_as, name='login_as'),
)
