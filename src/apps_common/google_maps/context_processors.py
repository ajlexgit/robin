from django.conf import settings


def google_apikey(request):
    return {
        'GOOGLE_APIKEY': settings.GOOGLE_APIKEY,
    }