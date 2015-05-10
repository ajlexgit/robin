from functools import wraps
from django.conf import settings
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from . import api


def permissions_possibly_required(function=None):
    perms = getattr(settings, 'GOOGLE_MAP_PERMISSIONS', None)
    if perms:
        actual_decorator = user_passes_test(perms)
        if function:
            return actual_decorator(function)
        return actual_decorator
    return function


def user_passes_test(perm_func):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if perm_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return _wrapped_view

    return decorator


@permissions_possibly_required
def get_coords(request):
    """
    Определение координат адреса для админки через AJAX.
    """
    address = request.POST.get('address', '')
    if not address:
        return HttpResponse()

    coords = api.geocode(address)
    if coords:
        return HttpResponse(', '.join(coords))
    return HttpResponse()
