from django.http.response import Http404
from django.shortcuts import get_object_or_404
from seo import Seo
from paginator import Paginator, EmptyPage
from libs.views import TemplateExView
from .models import BlogConfig, BlogPost, Tag


class IndexView(TemplateExView):
    config = None
    tag = None
    template_name = 'blog/index.html'

    def before_get(self, request, tag_slug=None):
        self.config = BlogConfig.get_solo()

        if tag_slug is not None:
            self.tag = get_object_or_404(Tag, slug=tag_slug)

    def get(self, request, tag_slug=None):
        if self.tag:
            posts = BlogPost.objects.filter(visible=True, tags=self.tag)
        else:
            posts = BlogPost.objects.filter(visible=True)

        try:
            paginator = Paginator(
                request,
                object_list=posts,
                per_page=3,
                page_neighbors=1,
                side_neighbors=1,
                allow_empty_first_page=False,
            )
        except EmptyPage:
            raise Http404

        # SEO
        seo = Seo()
        seo.set_data(self.config, defaults={
            'title': self.config.header,
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'tags': Tag.objects.active(),
            'current_tag': self.tag,
            'paginator': paginator,
        })


class DetailView(TemplateExView):
    config = None
    post = None
    template_name = 'blog/detail.html'

    def before_get(self, request, slug):
        self.config = BlogConfig.get_solo()
        self.post = get_object_or_404(BlogPost, slug=slug)

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