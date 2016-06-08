from django.conf.urls import url
from . import conf
from . import rss

feeds = {
    conf.NETWORK_GOOGLE: rss.GoogleFeed,
    conf.NETWORK_TWITTER: rss.TwitterFeed,
    conf.NETWORK_FACEBOOK: rss.FacebookFeed,
}


urlpatterns = [
    url(r'^rss/{}/$'.format(network), Feed(), name=network)
    for network, Feed in feeds.items()
]
