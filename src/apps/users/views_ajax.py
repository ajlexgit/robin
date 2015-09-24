from django.forms import model_to_dict
from django.views.generic.edit import FormView
from django.http import HttpResponse, Http404, JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from libs.views import TemplateExView, RenderToStringMixin
from libs.upload import upload_chunked_file, FileMissingError, NotLastChunk
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


class LoginView(RenderToStringMixin, FormView):
    """ AJAX login """
    template_name = 'users/ajax_login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return JsonResponse({
            'user': user_to_dict(user),
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.error_list,
            'form': self.render_to_string({
                'form': form,
            }),
        })


class LogoutView(TemplateExView):
    """ AJAX logout """
    def post(self, request):
        auth_logout(request)
        return JsonResponse({

        })


class RegisterView(RenderToStringMixin, FormView):
    """ AJAX register """
    template_name = 'users/ajax_register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            username=user.username,
            password=form.cleaned_data.get('password1')
        )
        auth_login(self.request, user)
        return JsonResponse({
            'user': user_to_dict(user),
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.error_list,
            'form': self.render_to_string({
                'form': form,
            }),
        })


class PasswordResetView(RenderToStringMixin, FormView):
    """ AJAX reset password """
    template_name = 'users/ajax_reset.html'
    form_class = PasswordResetForm
    email = ''

    def post(self, request, *args, **kwargs):
        self.email = request.POST.get('email', '')
        request.session['reset_email'] = self.email
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': default_token_generator,
            'email_template_name': 'users/reset_email.html',
            'subject_template_name': 'users/reset_subject.txt',
            'request': self.request,
            'html_email_template_name': 'users/reset_email.html',
        }
        form.save(**opts)
        return JsonResponse({
            'done': self.render_to_string({
                'email': self.email,
            }, template='users/ajax_reset_done.html'),
        })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': form.error_list,
            'form': self.render_to_string({
                'form': form,
            }),
        })


class AvatarUploadView(TemplateExView):
    """ Загрузка аватара """
    template_name = 'users/profile_avatar.html'

    def post(self, request):
        """ Загрузка автарки """
        if not request.user.is_authenticated():
            raise Http404

        try:
            uploaded_file = upload_chunked_file(request, 'image')
        except FileMissingError:
            raise Http404
        except NotLastChunk:
            return HttpResponse()

        request.user.avatar.save(uploaded_file.name, uploaded_file, save=False)
        uploaded_file.close()

        try:
            request.user.avatar.field.clean(request.user.avatar, request.user)
        except ValidationError as e:
            request.user.avatar.delete(save=False)
            return JsonResponse({
                'message': ', '.join(e.messages),
            }, status=400)

        request.user.avatar_crop = ''
        request.user.clean()
        request.user.save()

        return JsonResponse({
            'micro_avatar': request.user.micro_avatar,
            'small_avatar': request.user.small_avatar,
            'normal_avatar': request.user.normal_avatar,
            'profile_avatar_html': self.render_to_string({
                'profile_user': request.user,
            })
        })


class AvatarCropView(TemplateExView):
    """ Обрезка аватара """
    template_name = 'users/profile_avatar.html'

    def post(self, request):
        if not request.user.is_authenticated():
            raise Http404

        coords = request.POST.get('coords', '').split(':')
        try:
            coords = tuple(map(int, coords))
        except (TypeError, ValueError):
            raise Http404

        if len(coords) < 4:
            raise Http404
        else:
            coords = coords[:4]

        if not request.user.avatar:
            raise Http404

        request.user.avatar.recut(crop=coords)
        request.user.avatar_crop = ':'.join(map(str, coords))
        request.user.save()

        return JsonResponse({
            'micro_avatar': request.user.micro_avatar,
            'small_avatar': request.user.small_avatar,
            'normal_avatar': request.user.normal_avatar,
            'profile_avatar_html': self.render_to_string({
                'profile_user': request.user,
            })
        })


class AvatarRemoveView(TemplateExView):
    """ Удаление аватара """
    template_name = 'users/profile_avatar.html'

    def post(self, request):
        if not request.user.is_authenticated():
            raise Http404

        request.user.avatar.delete()

        return JsonResponse({
            'micro_avatar': request.user.micro_avatar,
            'small_avatar': request.user.small_avatar,
            'normal_avatar': request.user.normal_avatar,
            'profile_avatar_html': self.render_to_string({
                'profile_user': request.user,
            })
        })
