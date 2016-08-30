from django.conf.urls import url
from libs.autoslug import ALIAS_REGEXP
from . import views, cart


urlpatterns = [
    # AJAX
    url(r'^save-cart/$', cart.SaveCart.as_view(), name='save_cart'),
    url(r'^load-cart/$', cart.LoadCart.as_view(), name='load_cart'),
    url(r'^clear-cart/$', cart.ClearCart.as_view(), name='clear_cart'),
    
    url(
        r'^$', views.IndexView.as_view(),
        name='index'
    ),
    url(
        r'^(?P<category_slug>{0})/$'.format(ALIAS_REGEXP),
        views.CategoryView.as_view(),
        name='category'
    ),
    url(
        r'^(?P<category_slug>{0})/(?P<slug>{0})/$'.format(ALIAS_REGEXP),
        views.DetailView.as_view(),
        name='detail'
    ),
]
