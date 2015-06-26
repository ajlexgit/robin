from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class ColorWidget(forms.TextInput):
    """ Виджет цвета """

    input_type = 'color'

    class Media:
        css = {
            'all': (
                'color_field/admin/css/color.css',
            )
        }
        js = (
            'color_field/admin/js/color.js',
        )

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name, **{
            'class': 'colorfield-input input-small',
        })

        value = value or '#000000'
        value = force_text(value).upper()
        final_attrs['value'] = value

        return format_html((
            '<input {0} />&nbsp;<input {1} />'
        ), flatatt(final_attrs), flatatt({
            'type': 'text',
            'class': 'colorfield-text input-small',
            'pattern': '#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})',
            'maxlength': 7,
            'value': value,
        }))