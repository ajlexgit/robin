from django.conf import settings
from .js_storage import JSStorage
from . import JS_STORAGE


class JSStorageMiddleware:
    @staticmethod
    def process_request(request):
        request.js_storage = JSStorage(JS_STORAGE)
        request.js_storage.update({
            'cookie_domain': settings.SESSION_COOKIE_DOMAIN,
        })
