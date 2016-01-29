from django.contrib.sites.models import Site
import requests
from django.core.management import BaseCommand


class Command(BaseCommand):
    domain = ''
    default_protocol = 'http://'

    def __init__(self, *args, **kwargs):
        self.client = requests.Session()
        super().__init__(*args, **kwargs)

    def make_full_url(self, url):


    def get_page(self, url):
        full_url =

    def handle(self, *args, **options):
        site = Site.objects.first()
        self.domain = site.domain

        self.get_page('/')

        print('Done')
