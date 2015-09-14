from django.forms import ImageField
from .widgets import StdImageWidget


class StdImageFormField(ImageField):
    widget = StdImageWidget

    def __init__(self, *args, **kwargs):
        variations = kwargs.pop('variations')
        admin_variation = kwargs.pop('admin_variation')
        crop_area = kwargs.pop('crop_area')
        crop_field = kwargs.pop('crop_field')
        min_dimensions = kwargs.pop('min_dimensions')
        max_dimensions = kwargs.pop('max_dimensions')
        aspects = kwargs.pop('aspects', ())
        kwargs.pop('widget', None)
        super().__init__(*args, **kwargs)

        self.widget.context.update(
            variations=variations,
            admin_variation=variations[admin_variation],
            crop_area=crop_area,
            crop_field=crop_field,
            min_dimensions=min_dimensions,
            max_dimensions=max_dimensions,
        )

        if not isinstance(aspects, tuple):
            aspects = (aspects,)
        self.aspects = tuple(str(round(float(value), 4)) for value in aspects)
        self.widget.context['aspects'] = '|'.join(self.aspects)


    def clean(self, data, initial=None):
        final_data, delete, cropsize = data
        return (
            super().clean(final_data, initial),
            delete,
            cropsize
        )
