from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'shop'
    verbose_name = _('Shop')

    def ready(self):
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE
        from . import options

        JS_STORAGE.update({
            'save_cart': resolve_url('shop:save_cart'),
            'max_product_count': options.MAX_PRODUCT_COUNT,
        })