from .opengraph import Opengraph, TwitterCard
from . import OPENGRAPH


class OpengraphMiddleware:
    @staticmethod
    def process_request(request):
        request.opengraph = Opengraph(request)
        request.opengraph.update(OPENGRAPH)

        request.twitter_card = TwitterCard(request)
        request.twitter_card.update(OPENGRAPH)
