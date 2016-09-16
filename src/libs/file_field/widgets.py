from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


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
        template = '''<div class="file-widget">
            <button type="button" class="btn btn-success">
                <i class="icon-folder-open icon-white"></i>
                {label}
            </button>
            {input}
        </div>'''
        return mark_safe(template.format(
            label=_('Select file'),
            input=super().render(name, value, attrs),
        ))
