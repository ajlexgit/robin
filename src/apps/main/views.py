from django.views.generic import TemplateView
from seo import Seo
from .models import MainPageConfig


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        config = MainPageConfig.get_solo()

        # SEO
        seo = Seo()
        seo.set_data(config)
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'is_main_page': True,       # отменяет <noindex> шапки и подвала
        })
