from django.db import models
from django.core import validators
from .valute import Valute

DEFAULT_MAX_DIGITS = 18
DEFAULT_DECIMAL_PLACES = 2


class ValuteDescriptor():
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        value = instance.__dict__[self.field.name]
        if value is None:
            return None

        instance.__dict__[self.field.name] = Valute(value)
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        if value is not None:
            value = Valute(value)
        instance.__dict__[self.field.name] = value


class ValuteField(models.DecimalField):
    descriptor_class = ValuteDescriptor

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

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))
