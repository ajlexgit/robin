from django.conf.urls import url
from . import views_ajax


urlpatterns = [
    url(r'^get_coords/$', views_ajax.get_coords, name='get_coords'),
]