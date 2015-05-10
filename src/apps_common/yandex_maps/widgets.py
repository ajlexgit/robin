from django.conf import settings
from django.forms.widgets import TextInput


class YmapCoordsFieldWidget(TextInput):
    attrs = None

    class Media:
        js = (
            'http://api-maps.yandex.ru/2.0/?load=package.full&lang=%s' % settings.LANGUAGE_CODE,
            'yandex_maps/admin/js/init.js',
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'ymap_field',
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
