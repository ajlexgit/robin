from django.conf import settings
from django.forms.widgets import TextInput


class GoogleCoordsFieldWidget(TextInput):
    attrs = None

    class Media:
        js = (
            'google_maps/admin/js/init.js',
            '//maps.googleapis.com/maps/api/js?v=3.exp&language=%s' % settings.LANGUAGE_CODE,
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'google-map',
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
