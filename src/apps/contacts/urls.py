from django.conf.urls import url
from . import views, views_ajax


urlpatterns = [
    url(r'^ajax/$', views_ajax.ContactView.as_view(), name='ajax_contact'),

    url(r'^$', views.IndexView.as_view(), name='index'),
]
