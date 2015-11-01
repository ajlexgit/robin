from django import forms
from django.core import exceptions
from libs.coords import Coords
from .widgets import GoogleCoordsAdminWidget


class GoogleCoordsFormsField(forms.CharField):
    widget = GoogleCoordsAdminWidget

    def to_python(self, value):
        value = super().to_python(value)

        if not value:
            return None

        try:
            return Coords(*value.split(','))
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)
