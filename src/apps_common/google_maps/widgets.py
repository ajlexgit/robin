from django import forms


class GoogleCoordsFieldWidget(forms.TextInput):
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
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
