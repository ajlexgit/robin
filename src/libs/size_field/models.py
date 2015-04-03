import re
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .size import Size
from .forms import SizeFormField

re_size = re.compile('\d+x\d+')


class SizeField(models.Field, metaclass=models.SubfieldBase):
    min_width = 0
    min_height = 0
    max_width = 9999
    max_height = 9999
    default_error_messages = {
        'invalid_width': _('Width should be between %(min)s and %(max)s'),
        'invalid_height': _('Height should be between %(min)s and %(max)s'),
    }

    def __init__(self, *args, min_value=None, max_value=None, **kwargs):
        if isinstance(min_value, str):
            min_value = min_value.split('x')
        if isinstance(min_value, (list, tuple)):
            min_value = map(int, min_value)
        self.min_width, self.min_height = min_value

        if isinstance(max_value, str):
            max_value = max_value.split('x')
        if isinstance(max_value, (list, tuple)):
            max_value = map(int, max_value)
        self.max_width, self.max_height = max_value

        kwargs.setdefault('max_length', 9)

        super(SizeField, self).__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(re_size))

    def deconstruct(self):
        name, path, args, kwargs = super(SizeField, self).deconstruct()
        if kwargs['max_length'] == 9:
            del kwargs['max_length']

        if self.min_width != 0 or self.min_height != 0:
            kwargs['min'] = (self.min_width, self.min_height)

        if self.max_width != 9999 or self.max_height != 9999:
            kwargs['max'] = (self.max_width, self.max_height)

        return  name, path, args, kwargs

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if isinstance(value, Size):
            return value

        if not value:
            return None if self.null else ''

        if isinstance(value, str):
            value = value.split('x')

        width, height = tuple(map(int, value))

        if width < self.min_width or width > self.max_width:
            raise ValidationError(
                self.error_messages['invalid_width'],
                code='invalid_width',
                params=dict(min=self.min_width, max=self.max_width)
            )

        if height < self.min_height or height > self.max_height:
            raise ValidationError(
                self.error_messages['invalid_height'],
                code='invalid_height',
                params=dict(min=self.min_height, max=self.max_height)
            )

        return Size(width, height)

    def get_prep_value(self, value):
        if isinstance(value, (list, tuple)):
            return '%sx%s' % value
        elif isinstance(value, Size):
            return '{}x{}'.format(value.width, value.height)
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': SizeFormField,
            'min_width': self.min_width,
            'min_height': self.min_height,
            'max_width': self.max_width,
            'max_height': self.max_height,
        }
        defaults.update(kwargs)
        return super(SizeField, self).formfield(**defaults)
