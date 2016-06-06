from django.conf import settings
from django.views.generic import View
from django.http.response import StreamingHttpResponse, Http404
from .index import ALL_INDEXES, SphinxXMLIndex

SPHINX_SECRET = getattr(settings, 'SPHINX_SECRET', 'skvx8wjq8p81d')


class IndexPipeView(View):
    """ Вьюха, отдающая сфинксу XML индекса """
    def get(self, request, index_name, secret):
        if request.method.lower() == 'head':
            raise Http404

        if secret != SPHINX_SECRET:
            raise Http404

        if index_name not in ALL_INDEXES:
            raise Http404

        cls = ALL_INDEXES[index_name]
        if not issubclass(cls, SphinxXMLIndex):
            raise Http404

        index = cls()
        return StreamingHttpResponse(index.build_xml(), content_type='application/xml')
