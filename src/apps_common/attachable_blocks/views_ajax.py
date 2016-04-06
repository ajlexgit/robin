from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from .utils import get_block, get_block_view


class AsyncLoadView(AjaxViewMixin, View):

    def get(self, request):
        block_id = request.GET.get('block_id')
        try:
            block_id = int(block_id)
        except (TypeError, ValueError):
            return self.json_error(status=404)

        real_block = get_block(block_id)
        if not real_block or not real_block.visible:
            return self.json_error(status=404)

        block_view = get_block_view(real_block)
        if not block_view:
            return self.json_error(status=404)

        return self.json_response({
            'html': block_view(request, real_block)
        })
