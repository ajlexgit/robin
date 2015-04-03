from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth import get_backends, get_user_model, login, logout


@admin.site.admin_view
def login_as(request, user_id):
    """ Войти как... """
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        logout(request)
        return redirect(settings.LOGIN_URL)
    else:
        for backend in get_backends():
            if user == backend.get_user(user.pk):
                user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
                break
        
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
