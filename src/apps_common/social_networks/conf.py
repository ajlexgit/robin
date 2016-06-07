from django.conf import settings

# https://developers.facebook.com/apps/
# https://developers.facebook.com/tools/explorer/
FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID', getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', ''))
FACEBOOK_SECRET = getattr(settings, 'FACEBOOK_SECRET', getattr(settings, 'SOCIAL_AUTH_FACEBOOK_SECRET', ''))
FACEBOOK_TOKEN = getattr(settings, 'FACEBOOK_TOKEN', '')

# https://console.developers.google.com/apis/credentials
GOOGLE_APP_ID = getattr(settings, 'GOOGLE_KEY', getattr(settings, 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', ''))
GOOGLE_SECRET = getattr(settings, 'GOOGLE_SECRET', getattr(settings, 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', ''))

# https://apps.twitter.com/app
TWITTER_APP_ID = getattr(settings, 'TWITTER_APP_ID', getattr(settings, 'SOCIAL_AUTH_TWITTER_KEY', ''))
TWITTER_SECRET = getattr(settings, 'TWITTER_SECRET', getattr(settings, 'SOCIAL_AUTH_TWITTER_SECRET', ''))
TWITTER_TOKEN = getattr(settings, 'TWITTER_TOKEN', '')
TWITTER_TOKEN_SECRET = getattr(settings, 'TWITTER_TOKEN_SECRET', '')