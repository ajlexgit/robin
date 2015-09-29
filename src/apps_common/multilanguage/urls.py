from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^set/(?P<code>[-\w]{2,5})/$', views.set_lang, name='set_language'),
]
