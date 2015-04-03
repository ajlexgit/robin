from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .size import Size
from .widgets import SizeWidget


class SizeFormField(forms.Field):
    empty_values = forms.Field.empty_values + [['', '']]
    default_error_messages = {
        'not_number': _('Both values must be a numbers'),
        'invalid_width': _('Width should be between %(min)s and %(max)s'),
        'invalid_height': _('Height should be between %(min)s and %(max)s'),
    }

    def __init__(self, *args, min_width=0, max_width=9999, min_height=0, max_height=9999, **kwargs):
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        
        self.widget = SizeWidget(
            min_width = min_width,
            max_width = max_width,
            min_height = min_height,
            max_height = max_height,
        )
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        elif isinstance(value, str):
            return value.split('x')
        elif isinstance(value, (list, tuple)):
            return value
        elif isinstance(value, Size):
            return value.width, value.height
        
    def validate(self, value):
        super().validate(value)
        if value is None:
            return None
        
        try:
            value = tuple(map(int, value))
        except ValueError:
            raise ValidationError(self.error_messages['not_number'], code='not_number')
        
        if value[0] < self.min_width or value[0] > self.max_width:
            raise ValidationError(
                self.error_messages['invalid_width'], 
                code='invalid_width', 
                params=dict(min=self.min_width, max=self.max_width)
            )
        
        if value[1] < self.min_height or value[1] > self.max_height:
            raise ValidationError(
                self.error_messages['invalid_height'], 
                code='invalid_height',
                params=dict(min=self.min_height, max=self.max_height)
            )
            