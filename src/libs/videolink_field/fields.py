from django.db import models
from libs.widgets import URLWidget
from .videolink import VideoLink
from .formfields import VideoLinkFormField


class VideoLinkField(models.Field, metaclass=models.SubfieldBase):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 64
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        if value is None or value == '':
            return value
        if isinstance(value, VideoLink):
            return value
        return VideoLink(value)

    def get_prep_value(self, value):
        if value is None or value == '':
            return value
        if not isinstance(value, VideoLink):
            value = VideoLink(value)
        return value.db_value

    def clean(self, value, model_instance):
        return super().clean(value, model_instance)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': VideoLinkFormField,
            'widget': URLWidget(attrs={
                'class': 'input-xxlarge',
            }),
        })
        return super().formfield(**kwargs)
