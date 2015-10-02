from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^(?P<application>[\w\.]+)/(?P<model_name>\w+)/(?P<name>[-\w]+)/$',
        view=views.autocomplete_widget,
        name='autocomplete_widget'
    ),
)
