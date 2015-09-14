from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class StdImageWidget(forms.FileInput):
    class Media:
        js = (
            'admin/js/jquery.Jcrop.js',
            'admin/js/canvas_utils.js',
            'admin/js/cropdialog.js',
            'stdimage/admin/js/stdimage.js',
        )
        css = {
            'all': (
                'admin/css/jcrop/jquery.Jcrop.css',
                'admin/css/cropdialog/cropdialog.css',
                'stdimage/admin/css/stdimage.css',
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}

    def render(self, name, value, attrs=None):
        input_tag = super().render(name, value, dict(attrs, **{
            'class': 'uploader',
        }))

        context = dict(self.context, **{
            'name': name,
            'input': input_tag,
        })

        if value and hasattr(value, 'field'):
            context['value'] = value

        return mark_safe(render_to_string('stdimage/admin_widget.html', context))

    def value_from_datadict(self, data, files, name):
        return (
            super().value_from_datadict(data, files, name),
            data.get('%s-delete' % name, False),
            data.get('%s-croparea' % name, None)
        )
