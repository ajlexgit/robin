from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordResetForm as DefaultPasswordResetForm,
                                       SetPasswordForm as DefaultSetPasswordForm)
from libs.session_form import SessionStoredFormMixin
from libs.plainerror_form import PlainErrorFormMixin


class LoginForm(PlainErrorFormMixin, SessionStoredFormMixin, AuthenticationForm):
    error_messages = {
        'invalid_login': _('Login or password incorrect'),
        'inactive': _('Account blocked'),
    }

    username = forms.CharField(
        label=_('Login'),
        max_length=30,
        error_messages={
            'required': _('Please enter your login')
        }
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter your password')
        }
    )


class RegisterForm(PlainErrorFormMixin, SessionStoredFormMixin, UserCreationForm):
    error_messages = {
        'password_mismatch': _('The two passwords didn\'t match'),
    }

    username = forms.RegexField(
        label=_('Login'),
        min_length=3,
        max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'required': _('Please enter your login'),
            'unique': _('This login is already taken'),
            'invalid': _('Login must contain only letters, numbers ans sumbols @+-_'),
            'min_length': _('Login must be at least %(limit_value)s characters long'),
            'max_length': _('Login must be no more than %(limit_value)s characters'),
        }
    )
    email = forms.EmailField(
        label='E-mail',
        required=True,
        error_messages = {
            'required': _('Please enter your email'),
            'unique': _('This e-mail address is already taken'),
            'invalid': _('E-mail incorrect'),
        }
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as above, for verification.')
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def clean_username(self):
        UserModel = get_user_model()
        username = self.cleaned_data["username"]
        try:
            UserModel._default_manager.get(username=username)
        except UserModel.DoesNotExist:
            return username
        self.add_field_error('username', 'unique')

    def clean_email(self):
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        try:
            UserModel._default_manager.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return email
        self.add_field_error('email', 'unique')


class PasswordResetForm(PlainErrorFormMixin, DefaultPasswordResetForm):
    error_messages = {
        'unregistered_email': _('E-mail is not registered'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'E-mail'

    def clean_email(self):
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        try:
            UserModel._default_manager.get(email__iexact=email)
        except UserModel.DoesNotExist:
            self.add_field_error('email', 'unregistered_email')
        return email


class SetPasswordForm(PlainErrorFormMixin, DefaultSetPasswordForm):
    error_messages = {
        'password_mismatch': _('The two passwords didn\'t match'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password2'].label = _('Password confirmation')
