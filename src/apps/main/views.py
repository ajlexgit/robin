from django.views.generic import TemplateView
from libs.views import CachedViewMixin
from seo.seo import Seo
from .models import MainPageConfig


class IndexView(CachedViewMixin, TemplateView):
    template_name = 'main/index.html'
    config = None

    def last_modified(self, *args, **kwargs):
        self.config = MainPageConfig.get_solo()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'is_main_page': True,       # отменяет <noindex> шапки и подвала
        })
