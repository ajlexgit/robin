from django.core.cache import caches
from django.http.response import HttpResponseForbidden, JsonResponse
from . import conf

cache = caches[conf.CACHEBLOCK_BACKEND]

def get_cached(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    keys = request.GET.get('keys')
    if not keys:
        return JsonResponse({})

    try:
        keys = keys.split(',')
    except AttributeError:
        return HttpResponseForbidden()

    return JsonResponse({
        key: cache.get(key) or ''
        for key in keys
        if key
    })
