import requests
from libs.associative_request import associative
from .. import conf

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
    url = '%sv%d/%s' % (conf.API_URL, version, api_method)
    headers = {
        'X-MailerLite-ApiKey': conf.API_KEY,
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
