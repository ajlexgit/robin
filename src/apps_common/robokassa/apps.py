from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'robokassa'
    verbose_name = _('Robokassa')

    def ready(self):
        import robokassa.signals.handlers
