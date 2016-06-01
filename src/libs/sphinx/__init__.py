from .sphinxapi import SphinxClient, SPH_SORT_EXTENDED


class SphinxResult:
    __slots__ = ('_total', '_matches', '_ids')

    def __init__(self, data):
        data = data or {}
        self._total = data.get('total_found', 0)
        self._matches = data.get('matches', ())
        self._ids = None

    @property
    def total(self):
        """ Общее кол-во подходящих аргументов """
        return self._total

    @property
    def ids(self):
        """ Список ID найденных документов """
        if self._ids is None:
            self._ids = tuple(record['id'] for record in self)
        return self._ids

    def __iter__(self):
        return iter(self._matches)

    def __len__(self):
        """ Кол-во найденных элементов """
        return len(self._matches)


class SphinxIndex:
    model = None
    index = '*'
    limit = 250

    # defaults
    filters = ()
    weights = None
    order_by = '@relevance DESC, @id DESC'

    def __init__(self, host='localhost', port=9312):
        self.client = SphinxClient()
        self.client.SetServer(host, port)

    def fetch(self, query, filters=None, weights=None, order_by='', offset=0):
        """ Выборка страницы результатов """
        self.client.SetLimits(offset, self.limit)
        self.client.SetSortMode(SPH_SORT_EXTENDED, order_by or self.order_by)

        weights = weights or self.weights
        if weights:
            self.client.SetFieldWeights(weights)

        self.client.ResetFilters()
        filters = filters or self.filters
        for fieldname, values in filters:
            self.client.SetFilter(fieldname, values)

        return SphinxResult(self.client.Query(query, self.index))

    def fetch_models(self, query, *args, **kwargs):
        if self.model is None:
            raise RuntimeError("method SphinxIndex.fetch_models() requires 'model' attribute")

        page = self.fetch(query, *args, **kwargs)
        if not page:
            return ()

        qs = self.model._default_manager.filter(id__in=page.ids)
        qs_dict = {item.pk: item for item in qs}
        return (qs_dict[pk] for pk in page.ids)
