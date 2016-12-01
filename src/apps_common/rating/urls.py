from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^vote/$', views.VoteView.as_view(), name='vote'),
]