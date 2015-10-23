from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.http.response import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from libs.views import DecoratableViewMixin, AdminViewMixin, StringRenderMixin


class LazyJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super().default(obj)


class JSONError(Exception):
    def __init__(self, data, status=400):
        self.data = data
        self.status = status


class AjaxViewMixin(StringRenderMixin, DecoratableViewMixin):
    """
        Представление для обработки AJAX-запросов.
    """
    verify_ajax = True

    def get_handler(self, request):
        if self.verify_ajax and not request.is_ajax():
            return None
        else:
            return super().get_handler(request)

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except JSONError as e:
            return self.json_response(e.data, status=e.status)

    @staticmethod
    def json_response(data=None, **kwargs):
        if data is None:
            data = {}

        defaults = {
            'encoder': LazyJSONEncoder
        }
        defaults.update(kwargs)
        return JsonResponse(data, **defaults)


class AjaxAdminViewMixin(AdminViewMixin, AjaxViewMixin):
    pass
