from django import forms
from django.core import exceptions
from libs.coords import Coords
from .widgets import YandexCoordsAdminWidget


class YandexCoordsFormsField(forms.CharField):
    widget = YandexCoordsAdminWidget

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, Coords):
            return value

        try:
            return Coords(*value.split(','))
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)
