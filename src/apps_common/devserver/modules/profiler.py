import time
from functools import wraps
from contextlib import contextmanager
from django.db import connections
from django.utils.termcolors import colorize
from django.utils.decorators import available_attrs
from . import DevServerModule

_profiler_data = {}


def format_profile_info(name, data):
    """ Форматированние записи профайлера """
    calls = data['calls']
    if not calls:
        return

    total_time = data['time'] * 1000.0
    avg_time = total_time / calls

    msg = ("{funcname}\n"
           "    total time: {total_time} ({calls} calls)\n"
           "    avg time: {avg_time}\n"
           "    sql: {sql_time} ({sql} queries with {dupes} duplicates)")
    params = dict(
        funcname=colorize(name, fg='green', opts=('underscore',)),
        calls=calls,
        avg_time=colorize('%dms' % avg_time, fg='white'),
        total_time=colorize('%dms' % total_time, fg='white'),

        sql=data['sql'],
        dupes=data['sql'] - len(data['sql_unique']),
        sql_time=colorize('%dms' % data['sql_time'], fg='white'),
    )
    return msg.format(**params)


@contextmanager
def devprofile(name, summary=False):
    """
        Контекстный менеджер профилирования.

        Пример:
            with devprofiler('entity fetch'):
                e = Entity.objects.get(pk=1)
            ...
    """
    default = {
        'calls': 0,
        'time': 0,
        'sql': 0,
        'sql_unique': set(),
        'sql_time': 0,
        'sql_count': {},
    }

    if summary:
        data = _profiler_data.setdefault(name, default)
    else:
        data = default

    for dbname in connections:
        data['sql_count'][dbname] = len(connections[dbname].queries)

    start = time.time()
    yield
    end = time.time()

    for dbname in connections:
        queries = connections[dbname].queries[data['sql_count'][dbname]:]

        data['sql'] += len(queries)
        data['sql_unique'].update(q['sql'] for q in queries)
        data['sql_time'] += sum(float(c.get('time', 0)) for c in queries) * 1000

    data['calls'] += 1
    data['time'] += end - start

    if not summary:
        msg = format_profile_info(name, data)
        print(msg)


def devprofile_func(func):
    """
        Декоратор для профилирования функций.

        Пример:
            @devprofile
            def test(*args, **kwargs):
                ...
    """
    @wraps(func, assigned=available_attrs(func))
    def inner(*args, **kwargs):
        func_fullname = '%s.%s' % (func.__module__, func.__qualname__)
        with devprofiler(func_fullname):
            result = func(*args, **kwargs)
        return result
    return inner


class ProfilerModule(DevServerModule):
    """
        Вывод результатов профилирования
    """
    logger_name = 'profiler'

    def process_request(self, request):
        global _profiler_data
        _profiler_data = {}

    def process_response(self, request, response):
        global _profiler_data
        for funcname, data in sorted(_profiler_data.items()):
            msg = format_profile_info(funcname, data)
            if msg is None:
                continue

            self.logger.info(msg, multiline_indent=False)
        _profiler_data = {}

