from django import forms
from django.forms.widgets import FileInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class StdImageWidget(forms.ClearableFileInput):
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
        self.variations = kwargs.pop('variations')
        self.admin_variation = kwargs.pop('admin_variation')
        self.crop_area = kwargs.pop('crop_area')
        self.crop_field = kwargs.pop('crop_field')
        self.min_dimensions = kwargs.pop('min_dimensions')
        self.max_dimensions = kwargs.pop('max_dimensions')
        self.aspects = kwargs.pop('aspects')
        super().__init__(*args, **kwargs)
        
    def render(self, name, value, attrs=None):
        input_tag = super(FileInput, self).render(name, value, dict(attrs, **{
            'class': 'uploader',
        }))
        
        context = dict(
            name = name,
            input = input_tag,
            admin_variation = self.variations[self.admin_variation],
            crop_area = self.crop_area,
            crop_field = self.crop_field,
            min_dimensions = self.min_dimensions,
            max_dimensions = self.max_dimensions,
            aspects = '|'.join(self.aspects),
        )
        if value and hasattr(value, 'field'):
            context['value'] = value

        return mark_safe(render_to_string('stdimage/admin_widget.html', context))

    def value_from_datadict(self, data, files, name):
        return (
            super().value_from_datadict(data, files, name),
            data.get('%s-delete' % name, False),
            data.get('%s-croparea' % name, None)
        )
