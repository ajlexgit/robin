from django.views.generic.base import TemplateView
from haystack.query import SearchQuerySet
from haystack.generic_views import SearchMixin


class SearchView(SearchMixin, TemplateView):
    template_name = 'search/search.html'

    def get(self, request):
        query = request.GET.get('q')
        if query:
            queryset = SearchQuerySet()
            queryset = queryset.auto_query(query)
            queryset = queryset.load_all()
        else:
            queryset = None

        return self.render_to_response({
            'query': query,
            'queryset': queryset,
        })

