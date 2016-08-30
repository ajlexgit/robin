from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'shop'
    verbose_name = _('Shop')

    def ready(self):
        import shop.signals.handlers
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE
        from . import conf

        JS_STORAGE.update({
            'save_cart': resolve_url('shop:save_cart'),
            'load_cart': resolve_url('shop:load_cart'),
            'clear_cart': resolve_url('shop:clear_cart'),
            'max_product_count': conf.MAX_PRODUCT_COUNT,
        })
