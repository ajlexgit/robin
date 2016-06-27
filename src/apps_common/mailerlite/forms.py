from django import forms
from form_helper import FormHelperMixin
from .models import Subscriber


class SubscribeForm(FormHelperMixin, forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('groups', 'email', )
        widgets = {
            'groups': forms.MultipleHiddenInput,
        }

