from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordResetForm as DefaultPasswordResetForm,
                                       SetPasswordForm as DefaultSetPasswordForm)
from libs.session_form import SessionStoredFormMixin
from libs.plainerror_form import PlainErrorFormMixin

UserModel = get_user_model()


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
            'required': _('Please enter your e-mail'),
            'unique': _('This e-mail address is already taken'),
            'invalid': _('E-mail incorrect'),
        }
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter your password'),
        }
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        help_text=_('Enter the same password as above, for verification.'),
        error_messages={
            'required': _('Please enter password confirmation'),
        }
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            UserModel._default_manager.get(username=username)
        except UserModel.DoesNotExist:
            return username
        self.add_field_error('username', 'unique')

    def clean_email(self):
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

    email = forms.EmailField(
        label=_("E-mail"),
        max_length=254,
        error_messages={
            'required': _('Please enter your e-mail'),
            'invalid': _('E-mail incorrect'),
        }
    )

    def clean_email(self):
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

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter your password'),
        }
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        widget=forms.PasswordInput,
        error_messages={
            'required': _('Please enter password confirmation'),
        }
    )
