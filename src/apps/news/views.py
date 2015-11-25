from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from seo import Seo
from libs.views import TemplateExView
from .models import NewsPageConfig, Post


class IndexView(TemplateExView):
    config = None
    template_name = 'news/index.html'

    def before_get(self, request):
        self.config = NewsPageConfig.get_solo()

    def get(self, request):
        # SEO
        seo = Seo()
        seo.set_data(self.config, defaults={
            'title': self.config.header
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
        })


class DetailView(TemplateExView):
    config = None
    post = None
    template_name = 'news/detail.html'

    def before_get(self, request, slug):
        self.config = NewsPageConfig.get_solo()
        self.post = get_object_or_404(Post, slug=slug)

    def get(self, request, slug):
        # SEO
        seo = Seo()
        seo.set_title(self.config, default=self.config.header)
        seo.set_data(self.post, defaults={
            'title': self.post.title,
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'post': self.post,
        })
