from django.conf.urls import patterns, url
from . import views, views_ajax


urlpatterns = patterns('',
    # Ajax blocks
    url(r'^async/$', views_ajax.AsyncHeader.as_view(), name='async'),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<post_id>\d+)/$', views.DetailView.as_view(), name='detail'),
)
