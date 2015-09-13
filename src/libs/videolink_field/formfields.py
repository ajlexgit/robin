from django import forms
from django.core.exceptions import ValidationError
from .videolink import VideoLink


class VideoLinkFormField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        try:
            VideoLink(value)
        except ValueError as e:
            raise ValidationError(*e.args)
