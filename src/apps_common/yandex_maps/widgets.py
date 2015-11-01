from django import forms
from django.conf import settings


class YandexCoordsAdminWidget(forms.TextInput):
    attrs = None

    class Media:
        js = (
            'yandex_maps/js/core.js',
            'yandex_maps/admin/js/yandex_maps.js',
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'yandex-map-field',
            'data-width': getattr(settings, 'ADMIN_YANDEX_MAP_WIDTH', ''),
            'data-height': getattr(settings, 'ADMIN_YANDEX_MAP_HEIGHT', ''),
        }
        if attrs:
            defaults.update(attrs)

        super().__init__(defaults)
