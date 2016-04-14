from django.conf.urls import url
from libs.autoslug import ALIAS_REGEXP
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^by-tag/(?P<tag_slug>{0})/$'.format(ALIAS_REGEXP), views.IndexView.as_view(), name='tag'),
    url(r'^(?P<slug>{0})/$'.format(ALIAS_REGEXP), views.DetailView.as_view(), name='detail'),
]
