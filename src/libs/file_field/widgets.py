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
        template = '''<div class="file-widget {classes}">
            <label for="{for_label}" class="btn btn-small btn-success">
                <i class="icon-folder-open icon-white"></i>
                {btn_label}
                {input}
            </label>
            <a href="{view_url}" target="_blank" class="view-link btn btn-small btn-info" title="{view_title}"></a>
        </div>'''

        data = dict(
            classes='has-value' if value else '',
            for_label=attrs.get('id', ''),
            btn_label=_('Select file'),
            input=super().render(name, value, attrs),
            view_url=value.url if value else '#',
            view_title=_('View file'),
        )

        return mark_safe(template.format(**data))
