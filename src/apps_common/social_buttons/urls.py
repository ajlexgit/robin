from django.conf.urls import patterns, include, url
from . import views
from . import providers


urlpatterns = patterns('',
    url(r'^complete/$', views.CompleteView.as_view(), name='complete'),

    url(r'^google-oauth2/$', views.LoginView.as_view(), name='google_auth', kwargs={
        'provider_class': providers.GoogleProvider,
    }),
)
