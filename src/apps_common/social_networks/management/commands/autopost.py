import twitter
import logging
import facebook
from django.utils.timezone import now
from django.core.management import BaseCommand
from libs.description import description
from ...models import SocialPost
from ... import utils
from ... import conf

MAX_POSTS_PER_CALL = 3
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Autopost RSS feed to Twitter'
    facebook_api = None
    twitter_api = None

    def autopost_twitter(self):
        posts = SocialPost.objects.filter(for_network=conf.NETWORK_TWITTER)[:MAX_POSTS_PER_CALL]
        for post in posts:
            message = post.text
            if len(message) >= 140:
                message = description(message, 100, 138)

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
        self.facebook_api = facebook.GraphAPI(conf.FACEBOOK_TOKEN)
        self.autopost_facebook()

