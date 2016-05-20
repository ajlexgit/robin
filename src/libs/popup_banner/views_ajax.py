from django.http.response import Http404
from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin
from .models import Banner


class BannerView(AjaxViewMixin, View):
    def get(self, request):
        try:
            banner = Banner.objects.get(active=True, pk=request.GET.get('banner'))
        except Banner.DoesNotExist:
            raise Http404

        return self.json_response({
            'html': self.render_to_string('popup_banner/popup.html', {
                'banner': banner,
            }),
        })
