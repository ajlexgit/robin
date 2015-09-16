from .seo import Seo


class SeoMiddleware:
    @staticmethod
    def process_request(request):
        request.seo = Seo()
