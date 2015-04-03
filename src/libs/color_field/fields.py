from django.db import models
from django.core import validators
from .forms import ColorFormField


class ColorField(models.Field, metaclass=models.SubfieldBase):
    """
        Поле, хранящее цвет в формате #FFFFFF (в БД - FFFFFF).
    """

    default_validators = [
        validators.RegexValidator('^#[0-9A-F]{6}$')
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['max_length'] == 7:
            del kwargs['max_length']
        return name, path, args, kwargs

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        """ Добавляем решетку при отображении значения """
        value = super().to_python(value)
        if value and isinstance(value, str):
            value = value.upper().strip()
            if not value.startswith('#'):
                value = '#' + value

        return value

    def get_prep_value(self, value):
        """ При сохранении в БД убираем решетку """
        value = super().get_prep_value(value)
        if isinstance(value, str):
            if value.startswith('#'):
                value = value[1:]

        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': ColorFormField,
            'max_length': self.max_length,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
