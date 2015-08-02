from datetime import datetime
from django.utils.termcolors import colorize
from . import DevServerModule
from ..utils.time import ms_from_timedelta


class ProfileRenderModule(DevServerModule):
    """
        Вывод времени рендеринга страницы
    """
    start = 0
    logger_name = 'render'

    def process_request(self, request):
        self.start = datetime.now()

    def process_response(self, request, response):
        duration = datetime.now() - self.start
        duration_fmt = '%dms' % ms_from_timedelta(duration)
        self.logger.info(colorize(duration_fmt, fg='white'))

