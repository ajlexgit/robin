from django import forms
from .widgets import ColorWidget


class ColorFormField(forms.CharField):
    widget = ColorWidget

    def to_python(self, value):
        if value in self.empty_values:
            return ''
        if isinstance(value, list):
            return value[1]
        return value
