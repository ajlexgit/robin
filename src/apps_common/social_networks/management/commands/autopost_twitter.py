import twitter
from django.core.management import BaseCommand
from ... import utils
from ... import conf


class Command(BaseCommand):
    help = 'Autopost RSS feed to Twitter'

    def post(self, message, link=None):
        if link is not None:
            message += '\n%s' % utils.tinyurl(link)

        api = twitter.Api(conf.TWITTER_APP_ID, conf.TWITTER_SECRET, conf.TWITTER_TOKEN, conf.TWITTER_TOKEN_SECRET)
        api.PostUpdate(message)

    def handle(self, *args, **options):
        pass

