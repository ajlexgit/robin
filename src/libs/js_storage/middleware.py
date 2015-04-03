from .js_storage import JSStorage
from . import JS_STORAGE


class JSStorageMiddleware:
    @staticmethod
    def process_request(request):
        request.js_storage = JSStorage(JS_STORAGE)
