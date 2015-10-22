from django.conf.urls import url
from . import admin_views


urlpatterns = [
    url(r'^delete/$', admin_views.DeleteView.as_view(), name='delete'),
    url(r'^restore/$', admin_views.RestoreView.as_view(), name='restore'),
]
