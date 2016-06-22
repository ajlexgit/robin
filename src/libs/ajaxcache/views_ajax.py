from django.core.cache import caches
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseForbidden, JsonResponse
from . import conf

cache = caches[conf.AJAXCACHE_BACKEND]

@csrf_exempt
def get_cached(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    keys = request.GET.get('keys')
    if not keys:
        return JsonResponse({})

    keys = filter(lambda x: str(x).startswith('template.cache.'), keys.split(','))
    return JsonResponse({
        key: cache.get(key) or ''
        for key in keys
        if key
    })
