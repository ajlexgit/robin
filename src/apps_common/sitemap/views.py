from seo import Seo
from main.models import MainPageConfig
from libs.views import TemplateExView
from libs.cache import cached
from .models import SitemapConfig
from .map import Map


class IndexView(TemplateExView):
    config = None
    template_name = 'sitemap/index.html'

    def before_get(self, request):
        self.config = SitemapConfig.get_solo()

    @cached(time=30*60)
    def _build_map(self):
        """ Генерация карты """
        sitemap = Map()

        sitemap.add_child(MainPageConfig.get_solo())

        return sitemap

    def get(self, request):
        # SEO
        seo = Seo()
        seo.set_data(self.config, defaults={
            'title': self.config.header,
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'map': self._build_map(),
        })
