from django.db import models
from django.conf import settings
from .widgets import YandexCoordsFieldWidget


class Coords:
    _lat = None
    _lng = None

    def __init__(self, lng=None, lat=None):
        self.lng = lng
        self.lat = lat

    @property
    def lng(self):
        return self._lng

    @lng.setter
    def lng(self, value):
        try:
            self._lng = float(value)
        except (ValueError, TypeError):
            self._lng = None

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        try:
            self._lat = float(value)
        except (ValueError, TypeError):
            self._lat = None

    def __bool__(self):
        return self.lng is not  None and self.lat is not None

    def __iter__(self):
        if self:
            return iter((self._lng, self._lat))

    def __str__(self):
        if self:
            return '{0}, {1}'.format(self.lng, self.lat)
        else:
            return ''


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


class YandexCoordsField(models.CharField):
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
        kwargs['widget'] = YandexCoordsFieldWidget(attrs={
            'data-width': getattr(settings, 'ADMIN_YANDEX_MAP_WIDTH', ''),
            'data-height': getattr(settings, 'ADMIN_YANDEX_MAP_HEIGHT', ''),
        })
        return super().formfield(**kwargs)
