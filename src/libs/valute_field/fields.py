from django.db import models
from django.core import exceptions
from .valute import Valute

DEFAULT_MAX_DIGITS = 18
DEFAULT_DECIMAL_PLACES = 2


class ValuteField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 0
        kwargs['max_digits'] = DEFAULT_MAX_DIGITS
        kwargs['decimal_places'] = DEFAULT_DECIMAL_PLACES
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['default'] == 0:
            del kwargs['default']
        if kwargs['max_digits'] == DEFAULT_MAX_DIGITS:
            del kwargs['max_digits']
        if kwargs['decimal_places'] == DEFAULT_DECIMAL_PLACES:
            del kwargs['decimal_places']
        return name, path, args, kwargs

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return value

        try:
            return Valute(value)
        except (ValueError, TypeError):
            return None

    def to_python(self, value):
        if value is None:
            return None

        if isinstance(value, Valute):
            return value

        try:
            return Valute(value)
        except (TypeError, ValueError) as e:
            raise exceptions.ValidationError(e)

