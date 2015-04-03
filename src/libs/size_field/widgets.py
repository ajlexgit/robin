from django import forms
from suit.widgets import HTML5Input
from .size import Size


class SizeWidget(forms.MultiWidget):

    def __init__(self, attrs=None, min_width=0, max_width=9999, min_height=0, max_height=9999):
        widgets = (
            HTML5Input(input_type='number', attrs={
                'class': 'input-mini',
                'min': min_width,
                'max': max_width,
            }),
            HTML5Input(input_type='number', attrs={
                'class': 'input-mini',
                'min': min_height,
                'max': max_height,
            }),
        )
        super().__init__(widgets, attrs)

    def format_output(self, rendered_widgets):
        return '<span>&nbsp;x&nbsp;</span>'.join(rendered_widgets)

    def decompress(self, value):
        if isinstance(value, str):
            return value.split('x')
        elif isinstance(value, (list, tuple)):
            return value
        elif isinstance(value, Size):
            return value.width, value.height
        return [None, None]
        