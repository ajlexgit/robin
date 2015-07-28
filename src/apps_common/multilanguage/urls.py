from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^set/(?P<code>\w{1,5})/$', views.set_lang, name='set_language'),
)
