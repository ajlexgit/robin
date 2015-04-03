from django.conf.urls import patterns, url
from . import views_ajax


urlpatterns = patterns('',
    url(r'^refresh/$', views_ajax.RefreshView.as_view(), name='refresh'),
    url(r'^post/$', views_ajax.PostView.as_view(), name='post'),
    url(r'^change/$', views_ajax.ChangeView.as_view(), name='change'),
    url(r'^delete/$', views_ajax.DeleteView.as_view(), name='delete'),
    url(r'^restore/$', views_ajax.RestoreView.as_view(), name='restore'),
    url(r'^vote/$', views_ajax.VoteView.as_view(), name='vote'),
)
