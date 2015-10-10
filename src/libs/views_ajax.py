from libs.views import DecoratableViewMixin, StringRenderMixin


class AjaxViewMixin(StringRenderMixin, DecoratableViewMixin):
    """
        Представление для обработки AJAX-запросов.
    """
    verify_ajax = True

    def get_handler(self, request):
        if self.verify_ajax and not request.is_ajax():
            return None
        else:
            return super().get_handler(request)
