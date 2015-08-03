from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class ColorWidget(forms.TextInput):
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

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name, **{
            'class': 'colorfield-text input-small',
            'pattern': '#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})',
        })

        value = force_text(value).upper()
        final_attrs['value'] = value

        return format_html((
            '<input {0} />&nbsp;<input {1} />'
        ), flatatt({
            'type': 'color',
            'class': 'colorfield-input input-small',
            'value': value,
        }), flatatt(final_attrs))
