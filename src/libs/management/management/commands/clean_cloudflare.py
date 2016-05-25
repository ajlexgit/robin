import requests
from django.core import management

"""
    Очистка кэша CloudFlare
"""

API_KEY = 'a70a3ac797884ec445c639c6094dec1b4d2a7'
API_EMAIL = 'pix666@ya.ru'
ZONE_ID = '0c8ff4c7d3e346168fb1be781f63a295'


class Command(management.BaseCommand):

    def handle(self, *args, **options):
        url = 'https://api.cloudflare.com/client/v4/zones/{}/purge_cache'.format(ZONE_ID)
        headers = {
            'X-Auth-Email': API_EMAIL,
            'X-Auth-Key': API_KEY,
            'Content-Type': 'application/json',
        }
        params = '{"purge_everything":true}'
        resp = requests.delete(url, headers=headers, data=params)
        result = resp.json()
        print(result)
