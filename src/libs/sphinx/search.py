from .api import SphinxClient, SPH_SORT_EXTENDED
from .index import ALL_INDEXES


class SphinxSearchResult:
    __slots__ = ('_total', '_matches')

    def __init__(self, total_found=0, matches=()):
        self._total = total_found
        self._matches = tuple(matches)

    def __iter__(self):
        return iter(self._matches)

    def __len__(self):
        """ Кол-во найденных элементов """
        return len(self._matches)

    def __repr__(self):
        return '%s(%s)' % (str(type(self).__name__), self._matches)

    @property
    def total(self):
        """ Общее кол-во подходящих аргументов """
        return self._total


class SphinxSearch:
    index = '*'
    limit = 50
    index_attr_name = 'index_name'

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

        result = self.client.Query(query, self.index)
        return SphinxSearchResult(result['total_found'], result['matches'])

    def fetch_dicts(self, query, **kwargs):
        """ Обертка над fetch, возвращающая словари """
        result = self.fetch(query, **kwargs)
        return SphinxSearchResult(result.total, (
            {
                key: value.decode() if isinstance(value, bytes) else value
                for key, value in dict(record['attrs'], id=record['id']).items()
            }
            for record in self.fetch(query, **kwargs)
        ))

    def fetch_models(self, query, **kwargs):
        """ Обертка над fetch, возвращающая экземпляры моделей """
        result = self.fetch(query, **kwargs)

        order_list = tuple(
            (record['id'], record['attrs'][self.index_attr_name].decode())
            for record in result
        )

        index_ids = {}
        for record in order_list:
            index_ids.setdefault(record[1], []).append(record[0])

        index_instances = {}
        for index_name, ids in index_ids.items():
            index = ALL_INDEXES[index_name]

            # Выборка из БД
            qs_method = getattr(self, '%s_queryset' % index_name, None)
            if qs_method is None:
                qs = index.model._default_manager.filter(pk__in=ids)
            else:
                qs = qs_method(index.model, ids)

            for instance in qs:
                index_instances[(instance.id, index_name)] = instance

        return SphinxSearchResult(result.total, (
            index_instances[key_tuple]
            for key_tuple in order_list
            if key_tuple in index_instances
        ))
