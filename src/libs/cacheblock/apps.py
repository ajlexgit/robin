from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'libs.cacheblock'
    verbose_name = _('Cache Blocks')

    def ready(self):
        from django.shortcuts import resolve_url
        from django.core.cache import caches
        from libs.js_storage import JS_STORAGE
        from . import conf

        # Очитска кэша
        cache = caches[conf.CACHEBLOCK_BACKEND]
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern('template.cache.*')

        JS_STORAGE.update({
            'cacheblock_url': resolve_url('cacheblock:ajax'),
            'cacheblock_class': conf.CACHEBLOCK_CSS_CLASS,
        })
