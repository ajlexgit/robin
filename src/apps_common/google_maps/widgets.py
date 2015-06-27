from django import forms


class GoogleCoordsFieldWidget(forms.TextInput):
    attrs = None

    class Media:
        js = (
            'google_maps/admin/js/init.js',
        )

    def __init__(self, attrs=None):
        defaults = {
            'class': 'google-map',
        }
        if attrs:
            defaults.update(attrs)
        super().__init__(defaults)
