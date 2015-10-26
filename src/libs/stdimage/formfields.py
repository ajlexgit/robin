from django.forms import ImageField
from .widgets import StdImageWidget


class StdImageFormField(ImageField):
    widget = StdImageWidget

    def __init__(self, *args, **kwargs):
        variations = kwargs.pop('variations')
        admin_variation = kwargs.pop('admin_variation')
        crop_area = kwargs.pop('crop_area')
        min_dimensions = kwargs.pop('min_dimensions')
        max_dimensions = kwargs.pop('max_dimensions')
        aspects = kwargs.pop('aspects', ())
        super().__init__(*args, **kwargs)

        self.widget.context.update(
            variations=variations,
            preview_variation=variations.get(admin_variation),
            crop_area=crop_area,
            min_dimensions=min_dimensions,
            max_dimensions=max_dimensions,
        )

        if not isinstance(aspects, tuple):
            aspects = (aspects,)
        self.aspects = tuple(str(round(float(value), 4)) for value in aspects)
        self.widget.context['aspects'] = '|'.join(self.aspects)

    def clean(self, data, initial=None):
        croparea = None
        if isinstance(data, tuple):
            data, croparea = data

        result = super().clean(data, initial)
        return result, croparea
