from django import forms
from django.utils.translation import ugettext_lazy as _
from libs.form_helper.forms import FormHelperMixin
from .models import Group


class SubscribeForm(FormHelperMixin, forms.Form):
    field_template = 'form_helper/unlabeled_field.html'

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.MultipleHiddenInput,
    )

    email = forms.EmailField(
        required=True,
        label=_("E-mail"),
        widget=forms.EmailInput(attrs={
            'placeholder': 'E-mail',
            'required': True,
        }),
        error_messages={
            'unique': _("You're already subscribed"),
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['groups'] = Group.objects.filter(subscribable=True)
