from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from libs.coords import Coords
from .widgets import GoogleCoordsFieldWidget


class GoogleCoordsField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 32
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, *args, **kwargs):
        if not value:
            return None
        elif isinstance(value, str):
            return Coords(*value.split(','))
        else:
            raise TypeError('Invalid coordinates type: %r' % value)

    def get_prep_value(self, value):
        if not value:
            return ''
        elif isinstance(value, Coords):
            return str(value)
        else:
            raise TypeError('Invalid coordinates type: %r' % value)

    def to_python(self, value):
        if not value:
            return None
        elif isinstance(value, Coords):
            return value
        elif isinstance(value, str):
            try:
                return Coords(*value.split(','))
            except (TypeError, ValueError) as e:
                raise ValidationError(e)
        else:
            raise ValidationError('Invalid coordinates type: %r' % value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_db_prep_lookup(self, lookup_type, value, *args, **kwargs):
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def formfield(self, **kwargs):
        defaults = {
            'widget': GoogleCoordsFieldWidget(attrs={
                'data-width': getattr(settings, 'ADMIN_GOOGLE_MAP_WIDTH', ''),
                'data-height': getattr(settings, 'ADMIN_GOOGLE_MAP_HEIGHT', ''),
            })
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
