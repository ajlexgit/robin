from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'libs.boxberry'
    verbose_name = _('Boxberry')

    def ready(self):
        from libs.js_storage import JS_STORAGE
        from .conf import API_URL, API_TOKEN
        JS_STORAGE.update({
            'boxberry_url': API_URL,
            'boxberry_token': API_TOKEN,
        })
