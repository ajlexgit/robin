from .conf import GOOGLE_APIKEY


def google_apikey(request):
    return {
        'GOOGLE_APIKEY': GOOGLE_APIKEY,
    }