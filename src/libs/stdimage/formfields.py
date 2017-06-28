from django.forms import ImageField
from django.utils.translation import ugettext_lazy as _
from libs.variation_field import validation
from .widgets import StdImageWidget


class StdImageFormField(ImageField):
    widget = StdImageWidget

    def __init__(self, *args, **kwargs):
        variations = kwargs.pop('variations')
        admin_variation = kwargs.pop('admin_variation')
        crop_area = kwargs.pop('crop_area')
        aspects = kwargs.pop('aspects', ())
        self.min_dimensions = kwargs.pop('min_dimensions')
        self.max_dimensions = kwargs.pop('max_dimensions')
        self.max_size = kwargs.pop('max_size')
        super().__init__(*args, **kwargs)

        self.widget.context.update(
            variations=variations,
            preview_variation=variations.get(admin_variation),
            crop_area=crop_area,
            min_dimensions=self.min_dimensions,
            max_dimensions=self.max_dimensions,
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
        if result and (data or croparea):
            # валидировать, если изменился файл или область обрезки
            validation.validate_type(result,
                error_messages=self.error_messages
            )
            validation.validate_dimensions(result,
                min_dimensions=self.min_dimensions,
                max_dimensions=self.max_dimensions,
                croparea=croparea,
                error_messages=self.error_messages,
            )
            validation.validate_size(result,
                max_size=self.max_size,
                error_messages=self.error_messages,
            )

        return result, croparea

    def has_changed(self, initial, data):
        if isinstance(data, tuple):
            data, croparea = data
        return super().has_changed(initial, data)
