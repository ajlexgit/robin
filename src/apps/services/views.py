from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from libs.views import CachedViewMixin
from seo.seo import Seo
from .models import ServicesConfig, Service


class IndexView(CachedViewMixin, TemplateView):
    template_name = 'services/index.html'
    config = None

    def last_modified(self, *args, **kwargs):
        self.config = ServicesConfig.get_solo()
        return self.config.updated

    def get(self, request, *args, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.config, defaults={
            'title': self.config.header,
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'services': Service.objects.all(),
        })


class DetailView(CachedViewMixin, TemplateView):
    template_name = 'services/detail.html'
    config = None
    service = None

    def last_modified(self, *args, slug=None, **kwargs):
        self.config = ServicesConfig.get_solo()
        self.service = get_object_or_404(Service, slug=slug)
        return self.service.updated

    def get(self, request, *args, slug=None, **kwargs):
        # SEO
        seo = Seo()
        seo.set_data(self.service, defaults={
            'title': self.service.title,
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'service': self.service,
        })
