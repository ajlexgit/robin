from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(
        r'^ajax/cities/$',
        views.cities,
        name='cities'
    ),
    url(
        r'^ajax/cities_courier/$',
        views.cities_courier,
        name='cities_courier'
    ),
    url(
        r'^ajax/cities_full/$',
        views.cities_full,
        name='cities_full'
    ),

    url(
        r'^ajax/points/(?P<city_id>\d+)/$',
        views.points,
        name='points'
    ),
    url(
        r'^ajax/point/(?P<point_id>\d+)/$',
        views.point,
        name='point'
    ),

    url(
        r'^ajax/cost/(?P<point_id>\d+)/$',
        views.cost,
        name='cost'
    ),
)
