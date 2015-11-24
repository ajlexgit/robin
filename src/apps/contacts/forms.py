from django import forms
from django.utils.translation import ugettext_lazy as _
from libs.plainerror_form import PlainErrorFormMixin


class ContactForm(PlainErrorFormMixin, forms.Form):
    name = forms.CharField(
        required=True,
        label=_('Name'),
        max_length=128,
        error_messages={
            'required': _('Please enter your email or phone so we can contact you'),
            'max_length': _('Phone number should not be longer than %(limit_value)d characters'),
        }
    )

    phone = forms.CharField(
        required=False,
        label=_('Phone'),
        max_length=32,
        error_messages={
            'required': _('Please enter your email or phone so we can contact you'),
            'max_length': _('Phone number should not be longer than %(limit_value)d characters'),
        }
    )

    email = forms.EmailField(
        required=False,
        label=_('E-mail'),
        max_length=64,
        error_messages={
            'required': _('Please enter your email or phone so we can contact you'),
            'max_length': _('Email should not be longer than %(limit_value)d characters'),
        }
    )

    message = forms.CharField(
        required=True,
        label=_('Message'),
        max_length=1024,
        widget=forms.Textarea(attrs={
            'rows': 5,
        }),
        error_messages={
            'required': _('Please enter your message'),
            'max_length': _('Message should not be longer than %(limit_value)d characters'),
        }
    )

    def clean(self):
        if 'phone' in self.cleaned_data and 'email' in self.cleaned_data:
            phone = self.cleaned_data.get('phone')
            email = self.cleaned_data.get('email')

            if not phone and not email:
                self.add_field_error('phone', 'required')
                self.add_field_error('email', 'required')

        return super().clean()