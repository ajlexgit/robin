from django.forms.widgets import TextInput


class YmapCoordFieldWidget(TextInput):
    attrs = None

    class Media:
        js = (
            'http://api-maps.yandex.ru/2.0/?load=package.full&lang=ru-RU',
            'yandex_maps/admin/js/init.js',
        )
    
    def __init__(self, attrs=None):
        defaults = {
            'class': 'ymap_field',
        }
        if attrs:
            defaults.update(attrs)
        super(YmapCoordFieldWidget, self).__init__(defaults)
