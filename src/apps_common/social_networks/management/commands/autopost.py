import twitter
import logging
import facebook
from PyLinkedinAPI.PyLinkedinAPI import PyLinkedinAPI
from django.utils.timezone import now
from django.core.management import BaseCommand
from libs.description import description
from ...models import FeedPost
from ... import conf

TWITTER_URL_LEN = 23
TWITTER_MAX_LEN = 140
LINKEDIN_MAX_LEN = 600
MAX_POSTS_PER_CALL = 3
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Autopost RSS feed to Twitter'
    facebook_api = None
    twitter_api = None
    linkedin_api = None

    def autopost_twitter(self):
        posts = FeedPost.objects.filter(for_network=conf.NETWORK_TWITTER)[:MAX_POSTS_PER_CALL]
        for post in posts:
            message = post.text

            # Проверка длинны
            message_len = len(message)
            if post.url:
                message_len += TWITTER_URL_LEN
            if message_len >= TWITTER_MAX_LEN:
                message = description(message, 100, TWITTER_MAX_LEN - TWITTER_URL_LEN - 1)

            if post.url:
                message += '\n%s' % post.url

            try:
                self.twitter_api.PostUpdate(message)
            except twitter.TwitterError as e:
                logger.error("Twitter Autopost: error on #{0.pk}: {1.args}".format(post, e))
            else:
                logger.info("Twitter Autopost: posted #{0.pk} ('{0}')".format(post))
                post.scheduled = False
                post.posted = now()
                post.save()

    def autopost_facebook(self):
        posts = FeedPost.objects.filter(for_network=conf.NETWORK_FACEBOOK)[:MAX_POSTS_PER_CALL]
        for post in posts:
            attachment = {}
            message = post.text

            if post.url:
                attachment['link'] = post.url

            try:
                self.facebook_api.put_wall_post(message=message, attachment=attachment)
            except facebook.GraphAPIError as e:
                logger.error("Facebook Autopost: error on #{0.pk}: {1.args}".format(post, e))
            else:
                logger.info("Facebook Autopost: posted #{0.pk} ('{0}')".format(post))
                post.scheduled = False
                post.posted = now()
                post.save()

    def autopost_linkedin(self):
        posts = FeedPost.objects.filter(for_network=conf.NETWORK_LINKEDIN)[:MAX_POSTS_PER_CALL]
        for post in posts:
            message = post.text

            # Проверка длинны
            message_len = len(message)
            if post.url:
                message_len += len(post.url) + 1
            if message_len >= LINKEDIN_MAX_LEN:
                message = description(message, 540, LINKEDIN_MAX_LEN)

            if post.url:
                message += '\n%s' % post.url

            try:
                self.linkedin_api.publish_profile_comment(message)
            except Exception as e:
                logger.error("Linkedin Autopost: error on #{0.pk}: {1.args}".format(post, e))
            else:
                logger.info("Linkedin Autopost: posted #{0.pk} ('{0}')".format(post))
                post.scheduled = False
                post.posted = now()
                post.save()

    def handle(self, *args, **options):
        # === Twitter ===
        self.twitter_api = twitter.Api(
            conf.TWITTER_APP_ID,
            conf.TWITTER_SECRET,
            conf.TWITTER_TOKEN,
            conf.TWITTER_TOKEN_SECRET
        )
        self.autopost_twitter()

        # === Facebook ===
        self.facebook_api = facebook.GraphAPI(conf.FACEBOOK_TOKEN)
        self.autopost_facebook()

        self.linkedin_api = PyLinkedinAPI(conf.LINKEDIN_TOKEN)
        self.autopost_linkedin()
