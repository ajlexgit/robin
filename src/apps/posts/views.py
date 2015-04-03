from django.utils.html import strip_tags
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from libs.description import description
from libs.hits.models import Hits
from social import social_buttons
from paginator import Paginator
from .models import *


class IndexView(TemplateView):
    """ Главная страница раздела """
    template_name = 'posts/index.html'

    def get(self, request):
        # Хлебные крошки
        request.breadcrumbs.add('Главная', 'index')
        request.breadcrumbs.add(_('Posts'))
        
        paginator = Paginator(request,
            object_list = Post.objects.filter(visible=True),
            per_page = 4,
        )

        return self.render_to_response({
            'paginator': paginator,
        })


class DetailView(TemplateView):
    """ Страница публикации """
    template_name = 'posts/detail.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)

        # Хлебные крошки
        request.breadcrumbs.add('Главная', 'index')
        request.breadcrumbs.add(_('Posts'), 'posts:index')
        request.breadcrumbs.add(post.title)

        # Seo
        request.seo.set(title=post.title)
        
        # Настройки соцкнопок
        social_settings = {
            'url': request.build_absolute_uri(),
            'title': post.title,
            'description': description(strip_tags(post.text), 50, 150),
        }
        if post.preview:
            social_settings['image'] = request.build_absolute_uri(post.preview.url)

        # Opengraph
        request.opengraph.update(social_settings)

        # Счетчик просмотров
        Hits.increment(post, type='view')

        return self.render_to_response({
            'post': post,
            'social_buttons': social_buttons(social_settings),
        })
