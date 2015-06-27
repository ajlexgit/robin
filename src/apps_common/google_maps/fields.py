from django.db import models
from django.conf import settings
from libs.coords import Coords
from .widgets import GoogleCoordsFieldWidget

class CoordsDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        value = instance.__dict__[self.field.name]

        if isinstance(value, str):
            value = value.split(',')

        instance.__dict__[self.field.name] = self.field.attr_class(*value)

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class GoogleCoordsField(models.CharField):
    descriptor_class = CoordsDescriptor
    attr_class = Coords

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 32)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['max_length'] == 32:
            del kwargs['max_length']
        return name, path, args, kwargs

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def formfield(self, **kwargs):
        kwargs['widget'] = GoogleCoordsFieldWidget(attrs={
            'data-width': getattr(settings, 'ADMIN_GOOGLE_MAP_WIDTH', ''),
            'data-height': getattr(settings, 'ADMIN_GOOGLE_MAP_HEIGHT', ''),
        })
        return super().formfield(**kwargs)

