from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .widgets import YandexCoordsFieldWidget


class YmapCoords():
    """ Класс для координат """
    lng = None
    lat = None
    wrong_format = False

    def __init__(self, coords=None):
        if not coords:
            return

        coords_list = coords.split(',')
        try:
            self.lng = float(coords_list[0].strip())
            self.lat = float(coords_list[1].strip())
        except (ValueError, TypeError):
            self.wrong_format = True

    def __bool__(self):
        return not self.lng is None and not self.lat is None

    def __iter__(self):
        return iter((self.lng, self.lat))
        
    def __str__(self):
        if self:
            return '{0}, {1}'.format(self.lng, self.lat)
        else:
            return ''


class YandexCoordsField(models.Field, metaclass=models.SubfieldBase):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 32)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value):
        """ Форматирование при чтении из БД """
        if isinstance(value, YmapCoords):
            return value
        elif isinstance(value, str):
            return YmapCoords(value.strip())
        else:
            return YmapCoords()

    def get_prep_value(self, value):
        """ При сохранении в БД """
        return str(value)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs['max_length'] == 32:
            del kwargs['max_length']
        return name, path, args, kwargs

    def validate(self, value, model_instance):
        if value.wrong_format:
            raise ValidationError('Invalid value')

        super().validate(value, model_instance)

    def formfield(self, **kwargs):
        kwargs['widget'] = YandexCoordsFieldWidget(attrs={
            'data-width': getattr(settings, 'ADMIN_YANDEX_MAP_WIDTH', ''),
            'data-height': getattr(settings, 'ADMIN_YANDEX_MAP_HEIGHT', ''),
        })
        return super().formfield(**kwargs)
