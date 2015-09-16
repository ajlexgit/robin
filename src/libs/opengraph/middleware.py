from .opengraph import Opengraph
from . import OPENGRAPH


class OpengraphMiddleware:
    @staticmethod
    def process_request(request):
        request.opengraph = Opengraph(OPENGRAPH)
