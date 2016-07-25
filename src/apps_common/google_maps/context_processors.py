from django.conf import settings


def google_apikey(request):
    return {
        'GOOGLE_APIKEY': getattr(settings, 'GOOGLE_APIKEY', ''),
    }