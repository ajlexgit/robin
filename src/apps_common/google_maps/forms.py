from django import forms
from django.core import exceptions
from libs.coords import Coords
from .widgets import GoogleCoordsAdminWidget


class GoogleCoordsFormsField(forms.CharField):
    widget = GoogleCoordsAdminWidget

    def __init__(self, *args, **kwargs):
        self.zoom = kwargs.pop('zoom')
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {
            'data-zoom': self.zoom,
        }

    def to_python(self, value):
        value = super().to_python(value)

        if not value:
            return None

        try:
            return Coords(*value.split(','))
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)
