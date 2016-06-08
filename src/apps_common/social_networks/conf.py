from django.utils.translation import ugettext_lazy as _


NETWORK_GOOGLE = 'google'
NETWORK_TWITTER = 'twitter'
NETWORK_FACEBOOK = 'facebook'

NETWORKS = (
    (NETWORK_GOOGLE, _('Google Plus')),
    (NETWORK_TWITTER, _('Twitter')),
    (NETWORK_FACEBOOK, _('Facebook')),
)
