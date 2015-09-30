from datetime import datetime
from django.utils.termcolors import colorize
from . import DevServerModule


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
        duration = (duration.seconds * 1000) + (duration.microseconds / 1000.0)
        self.logger.info(
            colorize(
                '{:.0f}ms'.format(duration),
                fg='white'
            )
        )
