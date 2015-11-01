from django import forms
from django.conf import settings


class GoogleCoordsAdminWidget(forms.TextInput):
    attrs = None

    class Media:
        css = {
            'all': (
                'google_maps/admin/css/google_maps.css',
            )
        }
        js = (
            'google_maps/js/core.js',
            'google_maps/admin/js/google_maps.js',
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'google-map-field',
            'data-width': getattr(settings, 'ADMIN_GOOGLE_MAP_WIDTH', ''),
            'data-height': getattr(settings, 'ADMIN_GOOGLE_MAP_HEIGHT', ''),
        }
        if attrs:
            defaults.update(attrs)

        super().__init__(defaults)
