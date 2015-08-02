from django import forms
from .widgets import GalleryWidget


class GalleryFormField(forms.ModelChoiceField):
    widget = GalleryWidget

    def _set_queryset(self, queryset):
        self.widget.queryset = queryset
        super()._set_queryset(queryset)

    queryset = property(forms.ModelChoiceField._get_queryset, _set_queryset)

