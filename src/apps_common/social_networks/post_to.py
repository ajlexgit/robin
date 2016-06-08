import twitter
import facebook
from django.utils.html import strip_tags
from . import conf
from .utils import tinyurl


class PostingError(Exception):
    @property
    def message(self):
        return self.args[0]


def require_conf(*args):
    """ Требование наличия параметров конфигурации """
    for key in args:
        value = getattr(conf, key, None)
        if not value:
            raise PostingError("%s required" % key)



def post_to_twitter(message, url=None, image=None):
    """ Постинг в Твиттер """
    require_conf('TWITTER_APP_ID', 'TWITTER_SECRET', 'TWITTER_TOKEN', 'TWITTER_TOKEN_SECRET')

    message = strip_tags(message)

    if url is not None:
        message += '\n%s' % tinyurl(url)

    if image is not None:
        raise PostingError("'image' not allowed for Twitter")

    api = twitter.Api(conf.TWITTER_APP_ID, conf.TWITTER_SECRET, conf.TWITTER_TOKEN, conf.TWITTER_TOKEN_SECRET)
    try:
        api.PostUpdate(message)
    except twitter.TwitterError as e:
        raise PostingError(e.message)


def post_to_facebook(message, url=None, image=None):
    """ Постинг в Фейсбук """
    require_conf('FACEBOOK_TOKEN')

    message = strip_tags(message)
    attachment = {}


    if url is not None:
        attachment['link'] = url

    if image is not None:
        attachment['picture'] = image

    graph = facebook.GraphAPI(conf.FACEBOOK_TOKEN)
    graph.put_wall_post(message=message, attachment=attachment)
