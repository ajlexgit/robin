from django import forms
from django.utils.translation import ugettext_lazy as _
from form_helper import FormHelperMixin
from .models import Subscriber, Group


class SubscribeForm(FormHelperMixin, forms.ModelForm):
    field_template = 'form_helper/unlabeled_field.html'

    class Meta:
        model = Subscriber
        fields = ('groups', 'email', )
        error_messages = {
            'email': {
                'unique': _("You're already subscribed"),
            }
        }
        widgets = {
            'groups': forms.MultipleHiddenInput,
            'email': forms.EmailInput(attrs={
                'placeholder': 'E-mail',
                'required': True,
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['groups'] = Group.objects.all()
