from django.db import models
from django.core.exceptions import ValidationError
from .widgets import ColorWidget, ColorOpacityWidget
from .color import Color


class ColorField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 12)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.max_length == 12:
            del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, *args, **kwargs):
        if not value:
            return None
        elif isinstance(value, str):
            try:
                return Color(value)
            except (ValueError, TypeError):
                return None
        else:
            raise ValueError('Invalid color type: %r' % value)

    def get_prep_value(self, value):
        if not value:
            return ''
        elif isinstance(value, Color):
            return value.db_value
        else:
            raise TypeError('Invalid color type: %r' % value)

    def to_python(self, value):
        if not value:
            return None
        elif isinstance(value, Color):
            return value
        elif isinstance(value, str):
            try:
                return Color(value)
            except (TypeError, ValueError) as e:
                raise ValidationError(e)
        else:
            raise ValidationError('Invalid color type: %r' % value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {
            'widget': ColorWidget,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class ColorOpacityField(ColorField):
    def formfield(self, **kwargs):
        defaults = {
            'widget': ColorOpacityWidget,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
