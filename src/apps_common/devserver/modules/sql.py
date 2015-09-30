from django.db import connections
from django.utils.termcolors import colorize
from ..modules import DevServerModule


class SQLSummaryModule(DevServerModule):
    """
        Вывод длительности всех запросов
    """
    logger_name = 'sql'

    def process_response(self, request, response):
        queries = [
            q for alias in connections
            for q in connections[alias].queries
        ]
        num_queries = len(queries)

        if num_queries:
            unique = set([s['sql'] for s in queries])

            sql_time = '%dms' % (sum(float(c.get('time', 0)) for c in queries) * 1000, )
            sql_time = colorize(sql_time, fg='white')

            self.logger.info('%(sql_time)s (%(calls)s queries with %(dupes)s duplicates)' % dict(
                sql_time=sql_time,
                calls=num_queries,
                dupes=num_queries - len(unique),
            ))
