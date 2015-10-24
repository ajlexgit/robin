from django import forms
from .models import ClientFormModel, ClientInlineFormModel


class MainForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image',
        required=False
    )

    class Meta:
        model = ClientFormModel
        fields = '__all__'


class InlineForm(forms.ModelForm):
    class Meta:
        model = ClientInlineFormModel
        fields = '__all__'


InlineFormSet = forms.inlineformset_factory(
    ClientFormModel,
    ClientInlineFormModel,
    InlineForm,
    extra=0,
    min_num=1,
    max_num=4,
    can_delete=True,
    validate_min=True,
    validate_max=True,
)
