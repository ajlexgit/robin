from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'social_networks'
    verbose_name = _('Social Network Feeds')
