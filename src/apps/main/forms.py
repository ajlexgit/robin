from django import forms
from django.forms.models import BaseInlineFormSet
from libs.session_form import SessionStoredFormMixin, SessionStoredFormSetMixin
from libs.plainerror_form import PlainErrorFormMixin
from .models import ClientFormModel, ClientInlineFormModel


class MainForm(PlainErrorFormMixin, SessionStoredFormMixin, forms.ModelForm):
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
