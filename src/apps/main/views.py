from django.views.generic import TemplateView
from .models import MainPageConfig


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request):
        config = MainPageConfig.get_solo()

        # SEO
        request.seo.set_instance(config)

        return self.render_to_response({
            'config': config,
            'address': 'Тольятти, Майский проезд 64',
        })
