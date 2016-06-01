import itertools
from django.views.generic.base import TemplateView
from blog.models import BlogPost
from careers.models import Career
from libs.sphinx import SphinxIndex


class BlogPostIndex(SphinxIndex):
    model = BlogPost
    index = 'blog'
    weights = {
        'title': 2,
        'text': 1,
    }


class CareerIndex(SphinxIndex):
    model = Career
    index = 'careers'
    weights = {
        'title': 2,
        'text': 1,
    }


class SearchView(TemplateView):
    template_name = 'search/search.html'

    def get(self, request):
        query = request.GET.get('q')
        if query:
            blogs = BlogPostIndex().fetch_models(query)
            careers = CareerIndex().fetch_models(query)
            queryset = itertools.chain(blogs, careers)
        else:
            queryset = None

        return self.render_to_response({
            'query': query,
            'queryset': queryset,
        })

