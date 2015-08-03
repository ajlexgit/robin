from django import forms
from suit.admin import SortableTabularInline
from .models import PageFile


class PageFileForm(forms.ModelForm):
    class Media:
        js = ('files/admin/js/files.js', )

    class Meta:
        model = PageFile
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'file-on-page'}),
            'displayed_name': forms.TextInput(attrs={'class': 'file-on-page-name input-xlarge'}),
        }


class PageFileInline(SortableTabularInline):
    model = PageFile
    form = PageFileForm
    extra = 0
    sortable = 'order'
