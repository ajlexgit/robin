import twitter
import facebook
from PyLinkedinAPI.PyLinkedinAPI import PyLinkedinAPI
from libs.description import description
from . import conf


def post_to_twitter(message, url=None):
    twitter_api = twitter.Api(
        conf.TWITTER_APP_ID,
        conf.TWITTER_SECRET,
        conf.TWITTER_TOKEN,
        conf.TWITTER_TOKEN_SECRET
    )

    # Проверка длинны
    message_len = len(message)
    if url:
        message_len += conf.TWITTER_URL_LEN
    if message_len >= conf.TWITTER_MAX_LEN:
        message = description(message, conf.TWITTER_START_CUT, conf.TWITTER_MAX_LEN - conf.TWITTER_URL_LEN - 1)

    if url:
        message += '\n%s' % url

    twitter_api.PostUpdate(message)


def post_to_facebook(message, url=None):
    facebook_api = facebook.GraphAPI(conf.FACEBOOK_TOKEN)

    attachment = {}
    if url:
        attachment['link'] = url

    facebook_api.put_wall_post(message=message, attachment=attachment)


def post_to_linkedin(message, url=None):
    linkedin_api = PyLinkedinAPI(conf.LINKEDIN_TOKEN)

    # Проверка длинны
    message_len = len(message)
    if url:
        message_len += len(url) + 1
    if message_len >= conf.LINKEDIN_MAX_LEN:
        message = description(message, conf.LINKEDIN_START_CUT, conf.LINKEDIN_MAX_LEN)

    if url:
        message += '\n%s' % url

    linkedin_api.publish_profile_comment(message)
