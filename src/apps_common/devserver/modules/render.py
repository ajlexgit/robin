from datetime import datetime
from django.utils.termcolors import colorize
from . import DevServerModule


class ProfileRenderModule(DevServerModule):
    """
        Вывод времени рендеринга страницы
    """
    start = 0
    view = 0
    render = 0
    logger_name = 'render'

    def process_request(self, request):
        self.start = datetime.now()

    def process_template_response(self, request, response):
        self.view = datetime.now()

    def process_response(self, request, response):
        self.render = datetime.now()

        view_duration = self.view - self.start
        view_duration = (view_duration.seconds * 1000) + (view_duration.microseconds / 1000.0)
        self.logger.info(
            colorize(
                '{:.0f}ms'.format(view_duration),
                fg='white'
            ),
            name='view'
        )

        render_duration = self.render - self.view
        render_duration = (render_duration.seconds * 1000) + (render_duration.microseconds / 1000.0)
        self.logger.info(
            colorize(
                '{:.0f}ms'.format(render_duration),
                fg='white'
            ),
            name='render'
        )
