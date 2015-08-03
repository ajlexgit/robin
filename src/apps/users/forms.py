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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Login')


class RegisterForm(PlainErrorFormMixin, SessionStoredFormMixin, UserCreationForm):
    error_messages = {
        'duplicate_username': _('Login already registered'),
        'duplicate_email': _('E-mail address already registered'),
        'password_mismatch': _('Passwords do not match'),
    }

    username = forms.RegexField(label=_('Login'), min_length=3, max_length=30,
        regex=r'^[\w.@+-]+$',
        error_messages={
            'invalid': _('Login must contain only letters, numbers ans sumbols @+-_'),
            'min_length': _('Login must be at least %(limit_value)s characters long'),
            'max_length': _('Login must be no more than %(limit_value)s characters'),
        })

    email = forms.EmailField(
        label='E-mail',
        required=True,
        error_messages = {
            'invalid': _('E-mail incorrect'),
        }
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Login')
        self.fields['password2'].label = _('Confirm password')

    def clean_username(self):
        UserModel = get_user_model()
        username = self.cleaned_data["username"]
        try:
            UserModel._default_manager.get(username=username)
        except UserModel.DoesNotExist:
            return username
        self.add_field_error('username', 'duplicate_username')

    def clean_email(self):
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        try:
            UserModel._default_manager.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return email
        self.add_field_error('email', 'duplicate_email')


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
        'password_mismatch': _('Passwords do not match'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password2'].label = _('Confirm password')
