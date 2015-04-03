import datetime
from . import options


class ResolutionMiddleware:
    @staticmethod
    def _get_resolution_cookie(request):
        current_resolution = request.COOKIES.get('resolution')
        if current_resolution is None:
            return None

        try:
            current_resolution = int(current_resolution)
        except (TypeError, ValueError):
            return None
        else:
            if current_resolution not in options.RESOLUTION_WIDTHS:
                return None
            else:
                return current_resolution

    def process_request(self, request):
        request.resolution = self._get_resolution_cookie(request)
        request.js_storage.update({
            'resolution': request.resolution,
            'resolutions': options.RESOLUTION_WIDTHS,
        })

    def process_response(self, request, response):
        # Удаляем куку с невалидным разрешением
        current_resolution = self._get_resolution_cookie(request)
        if current_resolution and request.COOKIES.get('resolution') is not None:
            response.set_cookie(
                'resolution',
                None,
                expires=datetime.datetime.utcfromtimestamp(0),
                domain=request.get_host()
            )

        return response
