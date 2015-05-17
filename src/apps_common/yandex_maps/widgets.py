from django.forms.widgets import TextInput


class YandexCoordsFieldWidget(TextInput):
    attrs = None

    class Media:
        js = (
            'yandex_maps/admin/js/init.js',
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'yandex-map',
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
