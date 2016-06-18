from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'libs.ajaxcache'
    verbose_name = _('AJAX Cache Blocks')

    def ready(self):
        from django.shortcuts import resolve_url
        from django.core.cache import caches
        from libs.js_storage import JS_STORAGE
        from . import conf

        # Очитска кэша
        cache = caches[conf.AJAXCACHE_BACKEND]
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern('template.cache.*')

        JS_STORAGE.update({
            'ajaxcache_url': resolve_url('ajaxcache:ajax'),
            'ajaxcache_class': conf.AJAXCACHE_CSS_CLASS,
        })
