from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'boxberry'
    verbose_name = _('Boxberry')

    def ready(self):
        from django.shortcuts import resolve_url
        from libs.js_storage import JS_STORAGE
        from .conf import KEY

        JS_STORAGE.update({
            'boxberry_key': KEY,
            'boxberry_cities_url': resolve_url('boxberry:cities'),
            'boxberry_points_url': resolve_url('boxberry:points', city_id='0'),
            'boxberry_point_url': resolve_url('boxberry:point', point_id='0'),
            'boxberry_cost_url': resolve_url('boxberry:cost', point_id='0'),
        })
