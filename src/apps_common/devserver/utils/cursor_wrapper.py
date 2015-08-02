import os
import inspect
from datetime import datetime
from django.conf import settings
from django.template import Node, base, debug
from django.db.backends import utils
from django.utils.termcolors import colorize
from .time import ms_from_timedelta

try:
    import sqlparse
except ImportError:
    class sqlparse:
        @staticmethod
        def format(text, *args, **kwargs):
            return text


BASE_PATTERN = settings.BASE_DIR
TEMPLATE_BASE = os.path.abspath(base.__file__)
TEMPLATE_DEBUG = os.path.abspath(debug.__file__)
DEVSERVER_SQL_MIN_DURATION = getattr(settings, 'DEVSERVER_SQL_MIN_DURATION', None)


class DevserverCursorWrapper(utils.CursorWrapper):
    def __init__(self, cursor, db, logger):
        super().__init__(cursor, db)
        self.logger = logger

    def execute(self, sql, params=()):
        start = datetime.now()
        try:
            return super().execute(sql, params)
        finally:
            stop = datetime.now()
            duration = ms_from_timedelta(stop - start)

            if DEVSERVER_SQL_MIN_DURATION is None or duration >= DEVSERVER_SQL_MIN_DURATION:
                formatted_sql = sql % (params if isinstance(params, dict) else tuple(params))
                if formatted_sql is not None:
                    message = sqlparse.format(formatted_sql, reindent=True, keyword_case='upper')

                    stack = []
                    stackframe = inspect.stack()[1:]
                    for record in stackframe:
                        frame, filename, lineno, funcname, lines, index = record
                        if filename in (TEMPLATE_BASE, TEMPLATE_DEBUG):
                            # Вызов из шаблона
                            node = frame.f_locals.get('node') or frame.f_locals.get('self')
                            if isinstance(node, Node):
                                loader = node.source[0]
                                offsets = node.source[1]
                                with open(loader.name, newline='') as source:
                                    start = source.read(offsets[0])
                                    line_num = start.count('\n') + 1
                                    token = source.read(offsets[1] - offsets[0])

                                caller = '%s (node %r, line %s)' % (loader.loadname, token, line_num)
                                stack.append(colorize(caller, fg='green'))
                                break
                        elif filename.startswith(BASE_PATTERN) and not 'devserver' in filename:
                            # Вызов из кода
                            filename = filename[len(BASE_PATTERN):]
                            caller = '%s (func %r, line %s)' % (filename, funcname, lineno)
                            stack.append(colorize(caller, fg='green'))

                    if stack:
                        stack = '\n'.join(reversed(stack))
                        message = '%s\n%s\n%s\n' % (stack, '-' * 10, message)
                    self.logger.debug(message, duration=duration)

    def executemany(self, sql, param_list):
        start = datetime.now()
        try:
            return super().executemany(sql, param_list)
        finally:
            stop = datetime.now()
            duration = ms_from_timedelta(stop - start)

            message = sqlparse.format(sql, reindent=True, keyword_case='upper')
            message = 'Executed %s times\n' % message

            self.logger.debug(message, duration=duration)
            self.logger.debug('Found %s matching rows', self.cursor.rowcount, duration=duration, id='query')
