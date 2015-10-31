from django import forms


class YandexCoordsFieldWidget(forms.TextInput):
    attrs = None

    class Media:
        js = (
            'yandex_maps/js/core.js',
            'yandex_maps/admin/js/yandex_maps.js',
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'yandex-map-field',
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
