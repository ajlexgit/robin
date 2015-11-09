from django.forms import model_to_dict
from django.http.response import Http404
from django.views.generic import View, FormView
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from libs.views_ajax import AjaxViewMixin
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk
from .forms import LoginForm, RegisterForm, PasswordResetForm


def user_to_dict(user):
    """ Вывод информации о юзере в формате, пригодном для JSON """
    user_dict = model_to_dict(user, fields=(
        'id', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser'
    ))
    user_dict.update(avatar={
        name: getattr(user.avatar, name).url
        for name in user.avatar.variations
        if hasattr(user.avatar, name)
    })
    return user_dict


class LoginView(AjaxViewMixin, FormView):
    """ AJAX login """
    form_class = LoginForm
    template_name = 'users/ajax_login.html'

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return self.json_response({
            'user': user_to_dict(user),
        })

    def form_invalid(self, form):
        return self.json_response({
            'errors': form.error_dict_full,
            'form': self.render_to_string(self.template_name, {
                'form': form,
            }),
        })


class LogoutView(AjaxViewMixin, View):
    """ AJAX logout """
    def post(self, request):
        auth_logout(request)
        return self.json_response()


class RegisterView(AjaxViewMixin, FormView):
    """ AJAX register """
    form_class = RegisterForm
    template_name = 'users/ajax_register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise Http404
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise Http404
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            username=user.username,
            password=form.cleaned_data.get('password1')
        )
        auth_login(self.request, user)
        return self.json_response({
            'user': user_to_dict(user),
        })

    def form_invalid(self, form):
        return self.json_response({
            'errors': form.error_dict_full,
            'form': self.render_to_string(self.template_name, {
                'form': form,
            }),
        })


class PasswordResetView(AjaxViewMixin, FormView):
    """ AJAX reset password """
    email = ''
    form_class = PasswordResetForm
    template_name = 'users/ajax_reset.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise Http404
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.email = request.POST.get('email', '')
        request.session['reset_email'] = self.email
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': default_token_generator,
            'email_template_name': 'users/emails/reset_email.html',
            'subject_template_name': 'users/emails/reset_subject.txt',
            'request': self.request,
            'html_email_template_name': 'users/emails/reset_email.html',
        }
        form.save(**opts)
        return self.json_response({
            'done': self.render_to_string('users/ajax_reset_done.html', {
                'email': self.email,
            }),
        })

    def form_invalid(self, form):
        return self.json_response({
            'errors': form.error_dict_full,
            'form': self.render_to_string(self.template_name, {
                'form': form,
            }),
        })


class AvatarUploadView(AjaxViewMixin, View):
    """ Загрузка аватара """
    def post(self, request):
        """ Загрузка автарки """
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        try:
            uploaded_file = upload_chunked_file(request, 'image')
        except TemporaryFileNotFoundError as e:
            return self.json_response({
                'message': str(e),
            }, status=400)
        except NotLastChunk:
            return self.json_response()

        request.user.avatar.save(uploaded_file.name, uploaded_file, save=False)
        uploaded_file.close()

        try:
            request.user.full_clean()
        except ValidationError as e:
            request.user.avatar.delete(save=False)
            return self.json_response({
                'message': ', '.join(e.messages),
            }, status=400)
        else:
            request.user.save()

        return self.json_response({
            'micro_avatar': request.user.micro_avatar,
            'small_avatar': request.user.small_avatar,
            'normal_avatar': request.user.normal_avatar,
            'profile_avatar_html': self.render_to_string('users/profile_avatar.html', {
                'profile_user': request.user,
            })
        })


class AvatarCropView(AjaxViewMixin, View):
    """ Обрезка аватара """
    def post(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        if not request.user.avatar:
            return self.json_response({
                'message': _('There are no avatar'),
            }, status=400)

        try:
            croparea = request.POST.get('coords', '')
        except ValueError:
            return self.json_response({
                'message': _('Croparea is empty'),
            }, status=400)

        request.user.avatar.recut(croparea=croparea)

        return self.json_response({
            'micro_avatar': request.user.micro_avatar,
            'small_avatar': request.user.small_avatar,
            'normal_avatar': request.user.normal_avatar,
            'profile_avatar_html': self.render_to_string('users/profile_avatar.html', {
                'profile_user': request.user,
            })
        })


class AvatarRemoveView(AjaxViewMixin, View):
    """ Удаление аватара """
    def post(self, request):
        if not request.user.is_authenticated():
            return self.json_response({
                'message': _('Authentication required'),
            }, status=401)

        request.user.avatar.delete()

        return self.json_response({
            'micro_avatar': request.user.micro_avatar,
            'small_avatar': request.user.small_avatar,
            'normal_avatar': request.user.normal_avatar,
            'profile_avatar_html': self.render_to_string('users/profile_avatar.html', {
                'profile_user': request.user,
            })
        })
