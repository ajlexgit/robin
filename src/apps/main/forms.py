from django import forms
from .models import ClientFormModel, ClientInlineFormModel


class MainForm(forms.ModelForm):
    class Meta:
        model = ClientFormModel


class InlineForm(forms.ModelForm):
    class Meta:
        model = ClientInlineFormModel


InlineFormSet = forms.inlineformset_factory(
    ClientFormModel,
    ClientInlineFormModel,
    InlineForm,
    extra=1,
    can_delete=True,
    max_num=4,
    validate_max=True,
    min_num=1,
    validate_min=True
)
