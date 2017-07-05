from django import forms
from django.utils.translation import ugettext_lazy as _
from libs.form_helper.forms import FormHelperMixin


class SearchForm(FormHelperMixin, forms.Form):
    csrf_token = False
    field_template = 'form_helper/unlabeled_field.html'

    q = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'required': True,
            'placeholder': _('Search'),
        })
    )
