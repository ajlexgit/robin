from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.http.response import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from libs.views import DecoratableViewMixin, StringRenderMixin


class LazyJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super().default(obj)



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

    @staticmethod
    def json_response(data=None, **kwargs):
        if data is None:
            data = {}

        defaults = {
            'encoder': LazyJSONEncoder
        }
        defaults.update(kwargs)
        return JsonResponse(data, **defaults)