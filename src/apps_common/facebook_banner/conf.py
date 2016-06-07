from django.conf import settings

# https://developers.facebook.com/apps/?action=create
FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', ''))

POPUP_TIMEOUT = 4000
