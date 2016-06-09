import twitter
import logging
import facebook
from django.core.cache import cache
from django.utils.timezone import now
from django.core.management import BaseCommand
from ...models import SocialPost
from ... import utils
from ... import conf

logger = logging.getLogger(__name__)

MAX_POSTS_PER_CALL = 3
FACEBOOK_CACHE_KEY = 'facebook_token'


class Command(BaseCommand):
    help = 'Autopost RSS feed to Twitter'
    facebook_api = None
    twitter_api = None

    def autopost_twitter(self):
        posts = SocialPost.objects.filter(for_network=conf.NETWORK_TWITTER)[:MAX_POSTS_PER_CALL]
        for post in posts:
            message = post.text
            if post.url:
                message += '\n%s' % utils.tinyurl(post.url)

            try:
                self.twitter_api.PostUpdate(message)
            except twitter.TwitterError as e:
                logger.error("Twitter Autopost: error on #{0.pk}: {1.args}".format(post, e))
                raise e
            else:
                logger.info("Twitter Autopost: posted #{0.pk} ('{0}')".format(post))
                post.scheduled = False
                post.posted = now()
                post.save()

    def autopost_facebook(self):
        posts = SocialPost.objects.filter(for_network=conf.NETWORK_FACEBOOK)[:MAX_POSTS_PER_CALL]
        for post in posts:
            attachment = {}
            message = post.text

            if post.url:
                attachment['link'] = post.url

            try:
                self.facebook_api.put_wall_post(message=message, attachment=attachment)
            except facebook.GraphAPIError as e:
                logger.error("Facebook Autopost: error on #{0.pk}: {1.args}".format(post, e))
                raise e
            else:
                logger.info("Facebook Autopost: posted #{0.pk} ('{0}')".format(post))
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
        if FACEBOOK_CACHE_KEY in cache:
            token = cache.get(FACEBOOK_CACHE_KEY)
        else:
            token = conf.FACEBOOK_TOKEN

        self.facebook_api = facebook.GraphAPI(token)
        new_token = self.facebook_api.extend_access_token(conf.FACEBOOK_APP_ID, conf.FACEBOOK_SECRET)['access_token']
        cache.set(FACEBOOK_CACHE_KEY, new_token, timeout=30 * 24 * 3600)
        self.autopost_facebook()

