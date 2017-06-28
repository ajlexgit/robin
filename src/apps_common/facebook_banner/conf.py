from django.conf import settings

# https://developers.facebook.com/apps/?action=create
FACEBOOK_BANNER_APP_ID = getattr(settings, 'FACEBOOK_BANNER_APP_ID', '')

POPUP_TIMEOUT = 4000
