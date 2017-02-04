from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseForbidden, JsonResponse
from .models import AttachableBlock
from .utils import get_model_by_ct, get_block_view


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

        block_ct_id = AttachableBlock.objects.filter(pk=block_id).values_list('block_content_type', flat=True).first()
        block_model = get_model_by_ct(block_ct_id)
        block = block_model.objects.get(pk=block_id)

        if not block.visible:
            continue

        block_view = get_block_view(block)
        if not block_view:
            continue

        result[block_id] = block_view(RequestContext(request, {
            'request': request,
        }), block)

    return JsonResponse(result)

