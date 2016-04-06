from django.http.response import Http404
from django.shortcuts import get_object_or_404
from seo import Seo
from paginator import Paginator, EmptyPage
from libs.views import TemplateExView
from .models import BlogConfig, BlogPost, Tag


class IndexView(TemplateExView):
    template_name = 'blog/index.html'

    def get(self, request, *args, tag_slug=None, **kwargs):
        config = BlogConfig.get_solo()

        if tag_slug is not None:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = BlogPost.objects.filter(visible=True, tags=tag)
        else:
            tag = None
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
        seo.set_data(config, defaults={
            'title': config.header,
        })
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'tags': Tag.objects.active(),
            'current_tag': tag,
            'paginator': paginator,
        })


class DetailView(TemplateExView):
    template_name = 'blog/detail.html'

    def get(self, request, *args, slug=None, **kwargs):
        config = BlogConfig.get_solo()
        post = get_object_or_404(BlogPost, slug=slug)

        # SEO
        seo = Seo()
        seo.set_title(config, default=config.header)
        seo.set_data(post, defaults={
            'title': post.title,
        })
        seo.save(request)

        return self.render_to_response({
            'config': config,
            'post': post,
        })
