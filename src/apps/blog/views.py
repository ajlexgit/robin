from django.db import models
from django.http.response import Http404
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from seo.seo import Seo
from paginator.utils import get_paginator_meta
from paginator.paginator import Paginator, EmptyPage
from libs.views import CachedViewMixin
from libs.description import description
from .models import BlogConfig, BlogPost, Tag


class IndexView(CachedViewMixin, TemplateView):
    template_name = 'blog/index.html'
    config = None
    posts = None
    tag = None

    def last_modified(self, *args, tag_slug=None, **kwargs):
        self.config = BlogConfig.get_solo()

        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            self.posts = BlogPost.objects.filter(visible=True, tags=self.tag)
        else:
            self.posts = BlogPost.objects.filter(visible=True)

        return self.config.updated, self.posts.aggregate(models.Max('updated'))['updated__max']

    def get(self, request, *args, tag_slug=None, **kwargs):
        try:
            paginator = Paginator(
                request,
                object_list=self.posts,
                per_page=3,
                page_neighbors=1,
                side_neighbors=1,
                allow_empty_first_page=False,
            )
        except EmptyPage:
            raise Http404

        # SEO
        seo = Seo()
        seo.set(get_paginator_meta(paginator))
        seo.set_data(self.config, defaults={
            'title': self.config.header,
            'og_title': self.config.header,
        })

        # Unique title
        title_appends = ' | '.join(filter(bool, [
            self.tag.title if self.tag else '',
            'Page %d/%d' % (paginator.current_page_number, paginator.num_pages)
            if paginator.current_page_number >= 2 else '',
        ]))
        if title_appends:
            default_title = seo.title.popleft()
            seo.title = '%s | %s' % (default_title, title_appends)
            seo.description = ''

        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'paginator': paginator,
            'tags': Tag.objects.active(),
            'current_tag': self.tag,
        })


class DetailView(CachedViewMixin, TemplateView):
    template_name = 'blog/detail.html'
    config = None
    post = None

    def last_modified(self, *args, slug=None, **kwargs):
        self.config = BlogConfig.get_solo()
        self.post = get_object_or_404(BlogPost, slug=slug)
        return self.config.updated, self.post.updated

    def get(self, request, *args, slug=None, **kwargs):
        # SEO
        seo = Seo()
        seo.set_title(self.config, default=self.config.header)
        seo.set_data(self.post, defaults={
            'title': self.post.header,
            'description': description(self.post.note, 50, 160),
            'og_title': self.post.header,
            'og_image': self.post.preview,
            'og_description': self.post.note,
        })
        seo.save(request)

        return self.render_to_response({
            'config': self.config,
            'post': self.post,
        })
