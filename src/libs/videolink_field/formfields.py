from django import forms
from django.core.exceptions import ValidationError
from .videolink import VideoLink


class VideoLinkFormField(forms.CharField):
    def __init__(self, *args, providers=set(), **kwargs):
        super().__init__(*args, **kwargs)
        self._providers = set(providers)

    def validate(self, value):
        super().validate(value)
        try:
            VideoLink(value, self._providers)
        except ValueError as e:
            raise ValidationError(*e.args)
