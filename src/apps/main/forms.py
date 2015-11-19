from django import forms
from libs.plainerror_form import PlainErrorFormMixin
from .models import ClientFormModel, ClientInlineFormModel


class MainForm(PlainErrorFormMixin, forms.ModelForm):
    class Meta:
        model = ClientFormModel
        fields = '__all__'
        widgets = {
            'count': forms.NumberInput(attrs={
                'max': 99,
            })
        }


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
