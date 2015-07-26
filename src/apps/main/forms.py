from django import forms
from django.utils.translation import ugettext_lazy as _


class MainForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=False
    )


class InlineForm(forms.Form):
    name = forms.CharField(
        label='Name',
        required=False
    )


InlineFormSet = forms.formset_factory(InlineForm,
    extra=1,
    can_order=False,
    can_delete=True,
    max_num=4,
    validate_max=True,
    min_num=2,
    validate_min=True
)
