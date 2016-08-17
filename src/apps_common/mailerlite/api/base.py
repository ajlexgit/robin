import requests
from django.conf import settings
from libs.associative_request import associative

__all__ = ['SubscribeAPIError', 'request']


class SubscribeAPIError(Exception):
    @property
    def code(self):
        return self.args[0]

    @property
    def message(self):
        return self.args[1]


def request(api_method, method='GET', params=None, data=None, version=2):
    """ Запрос к API """
    url = 'https://api.mailerlite.com/api/v%d/%s' % (version, api_method)
    headers = {
        'X-MailerLite-ApiKey': settings.MAILERLITE_APIKEY,
    }
    response = requests.request(method, url,
        headers=headers,
        params=associative(params),
        data=associative(data),
        timeout=(5, 10),
    )

    try:
        data = response.json()
    except ValueError:
        return None

    if 'error' in data:
        raise SubscribeAPIError(data['error']['code'], data['error']['message'])

    return data
