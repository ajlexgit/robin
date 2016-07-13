from django.conf import settings
from django.utils.translation import ugettext_lazy as _


#============================================================
#                   Автопостинг
#============================================================

# Все доступные соцсети для автопостинга
NETWORK_GOOGLE = 'google'
NETWORK_TWITTER = 'twitter'
NETWORK_FACEBOOK = 'facebook'
NETWORK_LINKEDIN = 'linkedin'
ALL_NETWORKS = (
    (NETWORK_FACEBOOK, _('Facebook')),
    (NETWORK_TWITTER, _('Twitter')),
    (NETWORK_GOOGLE, _('Google Plus')),
    (NETWORK_LINKEDIN, _('Linked In')),
)

# Имена соцсетей, доступных для автопостинга на текущем сайте
ALLOWED_NETWORK_NAMES = (
    NETWORK_GOOGLE,
    NETWORK_TWITTER,
    NETWORK_FACEBOOK,
    NETWORK_LINKEDIN,
)

# Часть ALL_NETWORKS, включающая только доступные сети (для choices в модели)
ALLOWED_NETWORKS = tuple(
    pair
    for pair in ALL_NETWORKS
    if pair[0] in ALLOWED_NETWORK_NAMES
)

# Максимальная длина текста для поста
TEXT_MAX_LENGTH = 2048

# ============== API KEYS =====================

# https://developers.facebook.com/apps/
# https://developers.facebook.com/docs/marketing-api/quickstart
FACEBOOK_TOKEN = getattr(settings, 'FACEBOOK_TOKEN', '')

# https://apps.twitter.com/app
TWITTER_APP_ID = getattr(settings, 'TWITTER_APP_ID', getattr(settings, 'SOCIAL_AUTH_TWITTER_KEY', ''))
TWITTER_SECRET = getattr(settings, 'TWITTER_SECRET', getattr(settings, 'SOCIAL_AUTH_TWITTER_SECRET', ''))
TWITTER_TOKEN = getattr(settings, 'TWITTER_TOKEN', '')
TWITTER_TOKEN_SECRET = getattr(settings, 'TWITTER_TOKEN_SECRET', '')

# https://www.linkedin.com/developer/apps/
# https://apigee.com/console/linkedin
LINKEDIN_TOKEN = getattr(settings, 'LINKEDIN_TOKEN', '')


# ============================================================
#                   Виджет Instagram
# ============================================================

INSTAGRAM_TOKEN = getattr(settings, 'INSTAGRAM_TOKEN', '')
