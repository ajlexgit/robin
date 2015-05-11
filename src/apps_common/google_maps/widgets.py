from django.conf import settings
from django.forms.widgets import TextInput


class GoogleCoordsFieldWidget(TextInput):
    attrs = None

    class Media:
        js = (
            'http://maps.googleapis.com/maps/api/js?v=3.exp&language=%s' % settings.LANGUAGE_CODE,
            'google_maps/admin/js/init.js',
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'gmap_field',
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
