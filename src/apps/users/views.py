from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import Http404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.views import logout as default_logout, password_reset, password_reset_confirm
from seo import Seo
from libs.session_form import SessionFormView
from .forms import LoginForm, RegisterForm, PasswordResetForm, SetPasswordForm


def get_redirect_url(request):
    redirect_to = request.POST.get(
        REDIRECT_FIELD_NAME,
        request.GET.get(REDIRECT_FIELD_NAME, '')
    )
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
    return redirect_to


class LoginView(SessionFormView):
    """ Страница авторизации """
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(get_redirect_url(request))

        # Seo
        seo = Seo()
        seo.set({
            'title': _('Authorization')
        })
        seo.save(request)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect(get_redirect_url(self.request))


class LogoutView(View):
    """ Выход из профиля """
    @staticmethod
    def post(request, *args, **kwargs):
        return default_logout(request, *args, **kwargs)


class RegisterView(SessionFormView):
    """ Страница регистрации """
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        # Seo
        seo = Seo()
        seo.set({
            'title': _('Registration')
        })
        seo.save(request)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            username=user.username,
            password=form.cleaned_data.get('password1')
        )
        auth_login(self.request, user)
        return redirect(get_redirect_url(self.request))


class PasswordResetView(View):
    """ Страница с формой ввода email для сброса пароля """
    @staticmethod
    def get(request):
        if request.user.is_authenticated():
            return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))

        # Seo
        seo = Seo()
        seo.set({
            'title': _('Reset password')
        })
        seo.save(request)

        return password_reset(request,
            template_name='users/reset.html',
            password_reset_form=PasswordResetForm,
            post_reset_redirect='users:reset_done',
        )

    @staticmethod
    def post(request):
        email = request.POST.get('email', '')
        request.session['reset_email'] = email

        # Seo
        seo = Seo()
        seo.set({
            'title': _('Reset password')
        })
        seo.save(request)

        return password_reset(request,
            template_name='users/reset.html',
            password_reset_form=PasswordResetForm,
            post_reset_redirect='users:reset_done',
            email_template_name='users/emails/reset_email.html',
            html_email_template_name='users/emails/reset_email.html',
            subject_template_name='users/emails/reset_subject.txt',
        )


class ResetDoneView(TemplateView):
    """ Страница с сообщением о том, что инструкции для сброса пароля отправлены на почту """
    template_name = 'users/reset_done.html'

    def get(self, request, *args, **kwargs):
        email = request.session.get('reset_email')
        if not email:
            return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

        # Seo
        seo = Seo()
        seo.set({
            'title': _('Reset password')
        })
        seo.save(request)

        return self.render_to_response({
            'email': email,
        })

    @staticmethod
    def post(request):
        return redirect(request.build_absolute_uri())


class ResetConfirmView(TemplateView):
    """ Страница с формой ввода нового пароля """
    template_name = 'users/reset_confirm.html'

    def get(self, request, uidb64=None, token=None):
        UserModel = get_user_model()

        # Seo
        seo = Seo()
        seo.set({
            'title': _('Reset password')
        })
        seo.save(request)

        if request.user.is_authenticated():
            # Смена своего пароля, если авторизованы
            form = SetPasswordForm(request.user)
            return self.render_to_response({
                'form': form,
            })
        else:
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = UserModel._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                user = None

            if user is None or not default_token_generator.check_token(user, token):
                return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

            return password_reset_confirm(request,
                uidb64=uidb64,
                token=token,
                template_name='users/reset_confirm.html',
                set_password_form=SetPasswordForm,
                post_reset_redirect='users:reset_complete',
            )

    def post(self, request, uidb64=None, token=None):
        # Seo
        seo = Seo()
        seo.set({
            'title': _('Reset password')
        })
        seo.save(request)

        if request.user.is_authenticated():
            # Смена своего пароля, если авторизованы
            form = SetPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('users:reset_complete')
            else:
                return self.render_to_response({
                    'form': form,
                })
        else:
            if uidb64 is None or token is None:
                return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

            return password_reset_confirm(request,
                uidb64=uidb64,
                token=token,
                template_name='users/reset_confirm.html',
                set_password_form=SetPasswordForm,
                post_reset_redirect='users:reset_complete',
            )


class ResetCompleteView(TemplateView):
    """ Страница с сообщением о успешной смене пароля """
    template_name = 'users/reset_complete.html'

    def get(self, request, *args, **kwargs):
        # Seo
        seo = Seo()
        seo.set({
            'title': _('Reset password')
        })
        seo.save(request)

        if request.user.is_authenticated():
            # Смена своего пароля, если авторизованы
            return self.render_to_response({
                'redirect': resolve_url('users:profile', username=request.user.username),
            })
        else:
            email = request.session.pop('reset_email', '')
            if not email:
                return redirect(resolve_url(settings.RESET_PASSWORD_REDIRECT_URL))

            return self.render_to_response({
                'redirect': resolve_url(settings.RESET_PASSWORD_REDIRECT_URL),
            })


class ProfileView(TemplateView):
    """ Страница профиля """
    template_name = 'users/profile.html'

    def get(self, request, username=None):
        request.js_storage.update(
            avatar_upload=resolve_url('users:avatar_upload'),
            avatar_crop=resolve_url('users:avatar_crop'),
            avatar_delete=resolve_url('users:avatar_delete'),
        )

        UserModel = get_user_model()
        if username:
            user = get_object_or_404(UserModel, username=username)
        elif not request.user.is_authenticated():
            raise Http404
        else:
            user = request.user

        # Seo
        seo = Seo()
        seo.set({
            'title': _('Profile of «%(username)s»') % {'username': user.username}
        })
        seo.save(request)

        return self.render_to_response({
            'profile_user': user,
        })
