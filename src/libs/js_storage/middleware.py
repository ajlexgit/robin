from . import JS_STORAGE


class JSStorageMiddleware:
    @staticmethod
    def process_request(request):
        request.js_storage = JS_STORAGE.copy()
