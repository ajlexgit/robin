from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'libs.ajax_cache'
    verbose_name = _('AJAX Cache Blocks')

    def ready(self):
        from django.shortcuts import resolve_url
        from django.core.cache import caches
        from libs.js_storage import JS_STORAGE
        from .conf import AJAX_CACHE_BACKEND

        cache = caches[AJAX_CACHE_BACKEND]
        cache.delete_pattern('template.cache.*')

        JS_STORAGE.update({
            'ajax_cache_block': resolve_url('ajax_cache:ajax'),
        })
