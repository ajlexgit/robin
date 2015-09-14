from django import forms
from libs.variation_field import *
from .widgets import GalleryWidget


class GalleryFormField(forms.ModelChoiceField):
    widget = GalleryWidget

    def __init__(self, *args, **kwargs):
        related_model = kwargs.pop('related_model')
        super().__init__(*args, **kwargs)

        self.widget.context.update(
            gallery_model=related_model,
            app_label=related_model._meta.app_label,
            model_name=related_model._meta.model_name,
            admin_item_size=related_model.ADMIN_ITEM_SIZE,
        )

        if related_model.IMAGE_MODEL:
            aspects = format_aspects(
                related_model.IMAGE_MODEL.ASPECTS,
                related_model.IMAGE_MODEL.VARIATIONS
            )
            self.widget.context['aspects'] = '|'.join(aspects)
            self.widget.context['min_dimensions'] = related_model.IMAGE_MODEL.MIN_DIMENSIONS
            self.widget.context['max_dimensions'] = related_model.IMAGE_MODEL.MAX_DIMENSIONS
            self.widget.context['max_size'] = related_model.IMAGE_MODEL.MAX_SIZE
            if related_model.IMAGE_MODEL.ADMIN_CLIENT_RESIZE:
                self.widget.context['max_source'] = related_model.IMAGE_MODEL.MAX_SOURCE_DIMENSIONS

    def _set_queryset(self, queryset):
        self.widget.queryset = queryset
        super()._set_queryset(queryset)

    queryset = property(forms.ModelChoiceField._get_queryset, _set_queryset)

