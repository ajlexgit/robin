from django.conf import settings

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', '')
POPUP_TIMEOUT = 4000
