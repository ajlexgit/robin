from django.views.generic.base import TemplateView
from django.http.response import HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from seo.seo import Seo
from paginator.paginator import Paginator
from libs.cache.cached import cached
from libs.sphinx.search import SphinxSearch, SearchError
from .forms import SearchForm


class ShopProductsSearch(SphinxSearch):
    index = 'shop_products'
    weights = {
        'title': 2,
        'text': 1,
    }


class SearchPaginator(Paginator):
    search_class = ShopProductsSearch
    _fictive = None

    @cached('self.query', 'self.search_class.index', time=10*60)
    def item_count(self):
        try:
            self._fictive = self.searcher.fetch(self.query, limit=0)
        except SearchError:
            return 0
        else:
            return self._fictive.total

    def __init__(self, *args, query=None, **kwargs):
        self.query = query
        self.searcher = self.search_class()
        kwargs['object_list'] = range(self.item_count())
        super().__init__(*args, **kwargs)

    def __bool__(self):
        return self.item_count() > 0

    def page(self, number):
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page

        try:
            items = self.searcher.fetch_models(self.query, offset=bottom, limit=self.per_page)
        except SearchError:
            items = ()

        return self._get_page(items, number, self)


class SearchView(TemplateView):
    template_name = 'search/result.html'

    def get(self, request, **kwargs):
        form = SearchForm(request.GET)
        if not form.is_valid():
            return HttpResponseForbidden()

        query = form.cleaned_data.get('q')
        paginator = SearchPaginator(
            request,
            query=query,
            per_page=20,
            page_neighbors=1,
            side_neighbors=1,
        )

        # SEO
        seo = Seo()
        seo.title = _('Search results')
        seo.save(request)

        return self.render_to_response({
            'form': form,
            'title': _('Search by «%s»') % query,
            'paginator': paginator,
        })
