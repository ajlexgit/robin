from django.conf import settings
from django.forms.widgets import TextInput


class YmapCoordsFieldWidget(TextInput):
    attrs = None

    class Media:
        js = (
            'yandex_maps/admin/js/init.js',
            '//api-maps.yandex.ru/2.0-stable/?load=package.standard&onload=init_yandex_maps&lang=%s' % settings.LANGUAGE_CODE,
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'yandex-map',
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
