import os
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class FileWidget(forms.FileInput):
    """ Виджет выбора файла """
    class Media:
        css = {
            'all': (
                'file_field/admin/css/file_widget.css',
            )
        }
        js = (
            'file_field/admin/js/file_widget.js',
        )

    def render(self, name, value, attrs=None):
        context = dict(
            value=value,
            input=super().render(name, value, attrs),
            for_label=attrs.get('id', ''),
            filename=os.path.basename(value.name) if value else '',
        )

        return mark_safe(render_to_string('file_field/admin/widget.html', context))
