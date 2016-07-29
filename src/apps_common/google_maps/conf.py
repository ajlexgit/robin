from django.conf import settings

GOOGLE_APIKEY = getattr(settings, 'GOOGLE_APIKEY', '')
