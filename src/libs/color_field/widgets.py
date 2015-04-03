from django import forms
from suit.widgets import HTML5Input


class ColorWidget(forms.MultiWidget):
    """ Виджет цвета """
    class Media:
        css = {
            'all': (
                'color_field/admin/css/color.css',
            )
        }
        js = (
            'color_field/admin/js/color.js',
        )
    
    def __init__(self, attrs=None):
        widgets = (
            HTML5Input(input_type='color', attrs={
                'class': 'colorfield-input input-small'
            }),
            forms.TextInput(attrs={
                'class': 'colorfield-text input-small',
                'pattern': '#?[0-9a-fA-F]{6}'
            })
        )
        super(ColorWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value, value
        else:
            return None, None

    def format_output(self, rendered_widgets):
        return '&nbsp;'.join(rendered_widgets)
