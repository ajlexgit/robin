from decimal import Decimal
from django.db import models
from django.core import validators
from .widgets import ColorWidget, ColorOpacityWidget
from .color import Color


class ColorField(models.Field, metaclass=models.SubfieldBase):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
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
        if isinstance(value, Color):
            return value
        return Color(value)
    
    def get_prep_value(self, value):
        if value is None or value == '':
            return value
        return value._color
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
    
    def formfield(self, **kwargs):
        kwargs.update({
            'widget': ColorWidget,
            'max_length': 7,
        })
        return super().formfield(**kwargs)


class ColorOpacityField(models.Field, metaclass=models.SubfieldBase):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 11
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
        if isinstance(value, Color):
            return value
        if isinstance(value, (list, tuple)):
            return Color(*value)
            
        if ':' in value:
            return Color(*value.split(':'))
        else:
            return Color(value)
            
    def get_prep_value(self, value):
        if value is None or value == '':
            return value
        return '{}:{}'.format(value._color, value._opacity)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
        
    def formfield(self, **kwargs):
        kwargs.update({
            'widget': ColorWidget,
            'max_length': 7,
        })
        return super().formfield(**kwargs)
