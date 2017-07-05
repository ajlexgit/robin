from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _
from paginator import Paginator
from seo.seo import Seo
from libs.cache import cached
from libs.sphinx.search import SphinxSearch, SearchError
from .forms import SearchForm


class BlogSearch(SphinxSearch):
    index = 'blog'
    weights = {
        'title': 2,
        'text': 1,
    }


class SearchPaginator(Paginator):
    search_class = BlogSearch

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
    template_name = 'search/search.html'

    def get(self, request, **kwargs):
        form = SearchForm(request.GET)
        is_searching = 'q' in request.GET

        # SEO
        seo = Seo()
        seo.title = _('Search results')
        seo.save(request)

        context = {
            'form': form,
            'is_searching': is_searching,
        }

        if is_searching:
            # поиск
            if form.is_valid():
                paginator = SearchPaginator(
                    request,
                    query=form.cleaned_data.get('q'),
                    per_page=20,
                    page_neighbors=1,
                    side_neighbors=1,
                )

                context.update(**{
                    'paginator': paginator,
                })

        # страница поиска
        return self.render_to_response(context)
