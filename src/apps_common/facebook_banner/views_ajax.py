from django.views.generic.base import View
from libs.views_ajax import AjaxViewMixin


class BannerView(AjaxViewMixin, View):
    def get(self, request):
        return self.json_response({
            'html': self.render_to_string('facebook_banner/banner.html'),
        })
