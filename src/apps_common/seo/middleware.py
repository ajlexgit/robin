from django import http
from django.conf import settings
from .models import Redirect


class RedirectMiddleware(object):
    def process_request(self, request):
        full_path = request.get_full_path()

        if settings.DEBUG:
            return 

        redirect = None
        try:
            redirect = Redirect.objects.get(old_path=full_path)
        except Redirect.DoesNotExist:
            pass

        if settings.APPEND_SLASH and not request.path.endswith('/'):
            # Try appending a trailing slash.
            path_len = len(request.path)
            full_path = full_path[:path_len] + '/' + full_path[path_len:]
            try:
                redirect = Redirect.objects.get(old_path=full_path)
            except Redirect.DoesNotExist:
                pass

        if redirect is None:
            return

        if redirect.new_path == '':
            return http.HttpResponseGone()

        if redirect.permanent:
            return http.HttpResponsePermanentRedirect(redirect.new_path)
        else:
            return http.HttpResponseRedirect(redirect.new_path)
