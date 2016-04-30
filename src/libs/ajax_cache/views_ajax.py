import time
from django.core.cache import caches
from django.utils.http import http_date
from django.views.generic.base import View
from libs.views import CachedViewMixin
from libs.views_ajax import AjaxViewMixin
from .conf import AJAX_CACHE_BACKEND


class AjaxCacheView(CachedViewMixin, AjaxViewMixin, View):
    def get(self, request):
        cache_key = request.GET['key']
        fragment_cache = caches[AJAX_CACHE_BACKEND]

        response = self.json_response({
            'html': fragment_cache.get(cache_key)
        })

        expires = fragment_cache.get('time.%s' % cache_key)
        if expires is not None:
            response['Cache-Control'] = 'private, max-age=%d, must-revalidate' % expires
            response['Expires'] = http_date(time.time() + expires)

        return response
