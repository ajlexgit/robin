from django.core.cache import caches
from django.views.decorators.cache import cache_control
from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from .conf import AJAX_CACHE_BACKEND


class AjaxCacheView(AjaxViewMixin, View):
    def get_handler(self, request):
        handler = super().get_handler(request)
        handler = cache_control(private=True, max_age=7 * 24 * 3600)(handler)
        return handler

    def get(self, request):
        cache_key = request.GET.get('key')
        if cache_key is None or not cache_key.startswith('template.cache.'):
            return self.json_error()

        fragment_cache = caches[AJAX_CACHE_BACKEND]

        return self.json_response({
            'html': fragment_cache.get(cache_key)
        })
