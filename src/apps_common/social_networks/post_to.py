import twitter
import facebook
import httplib2
import apiclient as google
from oauth2client.client import OAuth2WebServerFlow
from django.utils.html import strip_tags
from . import conf
from .utils import tinyurl

GOOGLE_SCOPES = ['https://www.googleapis.com/auth/plus.me', 'https://www.googleapis.com/auth/plus.stream.write']
GOOGLE_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'


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


def post_to_google(message, url=None, image=None):
    """ Постинг в Фейсбук """
    require_conf('GOOGLE_APP_ID', 'GOOGLE_SECRET')

    message = strip_tags(message)
    attachments = []

    if url is not None:
        attachments.append({
            'url': url,
            'objectType': 'article',
        })

    if image is not None:
        attachments.append({
            'url': image,
            'objectType': 'photo',
        })


    flow = OAuth2WebServerFlow(
        client_id=conf.GOOGLE_APP_ID,
        client_secret=conf.GOOGLE_SECRET,
        scope=GOOGLE_SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )
    auth_uri = flow.step1_get_authorize_url()
    print(auth_uri)
    code = input()

    credentials = flow.step2_exchange(code)
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = google.discovery.build('plusDomains', 'v1', http=http)
    activities = service.activities()
    activities.insert(
        userId='me',
        body={
            'object': {
                'originalContent': message,
                'attachments': attachments,
            },
            'access': {
                'items': [{
                    'type': 'domain'
                }],
                'domainRestricted': True
            }
        }).execute()

