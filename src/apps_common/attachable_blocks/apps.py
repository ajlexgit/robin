from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'attachable_blocks'
    verbose_name = _('Attachable blocks')
