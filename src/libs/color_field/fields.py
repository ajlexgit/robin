import re
from django.db import models
from django.core import validators
from .widgets import ColorWidget

re_color = re.compile('^#[0-9A-F]{6}$')
re_hexcolor = re.compile('^#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$')


class FileDescriptor(object):
    def __init__(self, field):
        self.field = field

    def get_formatted_color(self, value):
        if value is None:
            return None

        value = str(value)
        if value:
            # add hash
            if value[0] != '#':
                value = '#' + value

            # upper
            value = value.upper()

            # convert to long format
            color_match = re_hexcolor.match(value)
            if color_match:
                color = color_match.group(1)
                if len(color) == 3:
                    value = '#' + ''.join(letter * 2 for letter in color)
                return value

        return None if self.field.null else ''

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        value = instance.__dict__[self.field.name]
        instance.__dict__[self.field.name] = self.get_formatted_color(value)

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        value = self.get_formatted_color(value)
        instance.__dict__[self.field.name] = self.get_formatted_color(value)


class ColorField(models.CharField):
    descriptor_class = FileDescriptor

    default_validators = [
        validators.RegexValidator(re_color)
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['max_length'] == 7:
            del kwargs['max_length']
        return name, path, args, kwargs

    def contribute_to_class(self, cls, *args, **kwargs):
        super().contribute_to_class(cls, *args, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def formfield(self, **kwargs):
        kwargs.update({
            'widget': ColorWidget,
        })
        return super().formfield(**kwargs)