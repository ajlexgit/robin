from seo import Seo
from main.models import MainPageConfig
from libs.views import TemplateExView
from libs.cache import cached
from .models import SitemapConfig
from .map import Map


class IndexView(TemplateExView):
    template_name = 'sitemap/index.html'

    @cached(time=30*60)
    def _build_map(self):
        """ Генерация карты """
        sitemap = Map()

        sitemap.add_child(MainPageConfig.get_solo())

        return sitemap

    def get(self, request, *args, **kwargs):
        config = SitemapConfig.get_solo()

        # SEO
        seo = Seo()
        seo.set_data(config, defaults={
            'title': config.header,
        })
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'map': self._build_map(),
        })
