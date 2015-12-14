from django.conf.urls import url
from . import views_ajax


urlpatterns = [
    url(
        r'^async/$', views_ajax.AsyncLoadView.as_view(),
        name='async'
    ),
]
