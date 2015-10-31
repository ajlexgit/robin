from django import forms
from .widgets import ColorWidget, ColorOpacityWidget


class ColorFormField(forms.CharField):
    widget = ColorWidget


class ColorOpacityFormField(ColorFormField):
    widget = ColorOpacityWidget
