from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'ckeditor'
    verbose_name = _('CKEditor')

    def ready(self):
        from .signals import handlers
