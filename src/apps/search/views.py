from django.views.generic.base import TemplateView
from libs.sphinx import SphinxSearch


class MySphinxSearch(SphinxSearch):
    limit = 20
    weights = {
        'title': 2,
        'text': 1,
    }


class SearchView(TemplateView):
    template_name = 'search/search.html'

    def get(self, request):
        query = request.GET.get('q')
        if query:
            queryset = MySphinxSearch().fetch_models(query)
        else:
            queryset = None

        return self.render_to_response({
            'query': query,
            'queryset': queryset,
        })
