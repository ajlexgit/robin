from django.conf.urls import patterns, url
from libs.autoslug import ALIAS_REGEXP
from . import views, cart


urlpatterns = patterns('',
    # AJAX
    url(
        r'^save-cart/$',
        cart.save_cart,
        name='save_cart',
    ),

    url(
        r'^$', views.IndexView.as_view(),
        name='index'
    ),
    url(
        r'^(?P<category_alias>{0})/$'.format(ALIAS_REGEXP),
        views.CategoryView.as_view(),
        name='category'
    ),
    url(
        r'^(?P<category_alias>{0})/(?P<alias>{0})/$'.format(ALIAS_REGEXP),
        views.DetailView.as_view(),
        name='detail'
    ),
)