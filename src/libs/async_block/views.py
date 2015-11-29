from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin


class AsyncBlockView(AjaxViewMixin, View):
    """ Родительский класс для асинхронных блоков """
    referrer = ''
    allowed = ()    # Допустимые параметры

    def _filter_params(self, params):
        """ Фильтрация параметров """
        result = {}
        for key, value in tuple(params.items()):
            if key in self.allowed and value is not None:
                result[key] = value
        return result

    def render(self, request, **kwargs):
        """ Генерация блока """
        raise NotImplementedError

    def sync_render(self, request, **kwargs):
        """ Получение блока синхронно """
        self.referrer = request.build_absolute_uri()
        params = self._filter_params(kwargs)
        return self.render(request, **params)

    def post(self, request):
        """ Получение блока асинхронно """
        self.referrer = request.POST.get('referrer', '')
        params = self._filter_params(request.GET)
        return self.json_response({
            'html': self.render(request, **params),
        })
