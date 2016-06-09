import facebook
from django.core.management import BaseCommand
from ... import conf


class Command(BaseCommand):
    help = 'Autopost RSS feed to Facebook'

    def post(self, message, link=None):
        attachment = {}

        if link is not None:
            attachment['link'] = link

        graph = facebook.GraphAPI(conf.FACEBOOK_TOKEN)
        graph.put_wall_post(message=message, attachment=attachment)

    def handle(self, *args, **options):
        pass

