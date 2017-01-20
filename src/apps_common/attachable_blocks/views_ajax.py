from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseForbidden, JsonResponse
from .utils import get_block, get_block_view


@csrf_exempt
def get_blocks(request):
    if not request.is_ajax():
        return HttpResponseForbidden()

    keys = request.GET.get('keys')
    if not keys:
        return JsonResponse({})

    result = {}
    for block_id in keys.split(','):
        try:
            block_id = int(block_id)
        except (TypeError, ValueError):
            continue

        real_block = get_block(block_id)
        if not real_block or not real_block.visible:
            continue

        block_view = get_block_view(real_block)
        if not block_view:
            continue

        result[block_id] = block_view(RequestContext(request, {
            'request': request,
        }), real_block)

    return JsonResponse(result)

