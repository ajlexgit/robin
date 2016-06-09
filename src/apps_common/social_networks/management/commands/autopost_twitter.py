import twitter
from django.utils.timezone import now
from django.core.management import BaseCommand
from ...models import SocialPost
from ... import utils
from ... import conf


class Command(BaseCommand):
    help = 'Autopost RSS feed to Twitter'

    def share(self, message, link=None):
        if link is not None:
            message += '\n%s' % utils.tinyurl(link)

        api = twitter.Api(conf.TWITTER_APP_ID, conf.TWITTER_SECRET, conf.TWITTER_TOKEN, conf.TWITTER_TOKEN_SECRET)
        api.PostUpdate(message)

    def handle(self, *args, **options):
        posts = SocialPost.objects.filter(network=conf.NETWORK_TWITTER, scheduled=True)
        if not posts:
            print('There are no available posts')
            return

        for post in posts:
            try:
                self.share(post.text, post.url)
            except twitter.TwitterError as e:
                raise e
            else:
                post.posted = now()
                post.save()


