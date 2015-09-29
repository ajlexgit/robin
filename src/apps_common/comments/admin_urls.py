from django.conf.urls import url
from . import admin_views


urlpatterns = [
    url(r'^delete/$', admin_views.delete_comment, name='delete'),
    url(r'^restore/$', admin_views.restore_comment, name='restore'),
]
