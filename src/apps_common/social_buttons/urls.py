from django.conf.urls import patterns, include, url
from . import providers


urlpatterns = patterns('',
    # url(r'^complete/$', views.CompleteView.as_view(), name='complete'),
)


for name, provider in providers.PROVIDERS.items():
    urlpatterns += url(r'^{}-oauth2/$'.format(name), provider.redirect_view, name=name),
    urlpatterns += url(r'^{}-complete/$'.format(name), provider.info_view, name='%s-complete' % name),