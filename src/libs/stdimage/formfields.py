from django.forms import ImageField
from .widgets import StdImageWidget


class StdImageFormField(ImageField):
    def __init__(self, *args, **kwargs):
        # Форматируем кортеж аспектов
        aspects = kwargs.pop('aspects', ())
        if not isinstance(aspects, tuple):
            aspects = (aspects, )
        self.aspects = tuple(str(round(float(value), 4)) for value in aspects)
        
        kwargs['widget'] = StdImageWidget(
            variations = kwargs.pop('variations'),
            admin_variation = kwargs.pop('admin_variation'),
            crop_area = kwargs.pop('crop_area', False),
            crop_field = kwargs.pop('crop_field', None),
            min_dimensions = kwargs.pop('min_dimensions'),
            max_dimensions = kwargs.pop('max_dimensions'),
            aspects = self.aspects,
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        final_data, delete, cropsize = data
        return (
            super().clean(final_data, initial),
            delete, 
            cropsize
        )
