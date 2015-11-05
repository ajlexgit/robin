from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'header'
    verbose_name = _('Header')

    def ready(self):
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE

        JS_STORAGE.update({
            'update_header_auth': resolve_url('header:update_header_auth'),
        })
