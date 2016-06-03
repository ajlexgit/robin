from .opengraph import Opengraph, TwitterCard
from . import OPENGRAPH


class OpengraphMiddleware:
    @staticmethod
    def process_request(request):
        request.opengraph = Opengraph(OPENGRAPH)
        request.twitter_card = TwitterCard(OPENGRAPH)
