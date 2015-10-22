from django import forms
from django.forms.widgets import FILE_INPUT_CONTRADICTION
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class StdImageWidget(forms.FileInput):
    class Media:
        js = (
            'admin/js/jquery.Jcrop.js',
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

    def clear_checkbox_name(self, name):
        return name + '-delete'

    def value_from_datadict(self, data, files, name):
        upload = super().value_from_datadict(data, files, name)
        if not self.is_required and forms.CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False

        return (
            upload,
            data.get('%s-croparea' % name, None) or None
        )
