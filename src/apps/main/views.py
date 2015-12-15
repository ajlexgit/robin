from seo import Seo
from libs.views import TemplateExView
from .models import MainPageConfig


class IndexView(TemplateExView):
    config = None
    template_name = 'main/index.html'

    def before_get(self, request):
        self.config = MainPageConfig.get_solo()

    def get(self, request):
        # SEO
        seo = Seo()
        seo.set_data(self.config)
        seo.save(request)

        # Opengraph
        request.opengraph.update({
            'url': request.build_absolute_uri(),
            'title': 'Hello',
            'image': request.build_absolute_uri(self.config.preview.url),
            'description': 'Best site ever!',
        })

        return self.render_to_response({
            'config': self.config,
            'is_main_page': True,
        })
