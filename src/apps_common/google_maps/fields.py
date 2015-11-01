from django.db import models
from django.core import exceptions
from libs.coords import Coords


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

        try:
            return Coords(*value.split(','))
        except (ValueError, TypeError):
            return None

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if not value:
            return ''

        if not isinstance(value, Coords):
            value = Coords(*value.split(','))

        return str(value)

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, Coords):
            return value

        try:
            return Coords(*value.split(','))
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_db_prep_lookup(self, lookup_type, value, *args, **kwargs):
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)
