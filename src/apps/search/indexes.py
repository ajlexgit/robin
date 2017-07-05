from libs.sphinx.index import SphinxScheme, SphinxXMLIndex, ATTR_TYPE
from blog.models import BlogPost


class SearchScheme(SphinxScheme):
    def __init__(self, index_name):
        super().__init__(index_name)
        self.add_fields('title', is_attribute=True)
        self.add_fields('text')
        self.add_attr('url')


class BlogIndex(SphinxXMLIndex):
    name = 'blog'
    model = BlogPost
    scheme_class = SearchScheme

    def get_queryset(self):
        return self.model.objects.filter(visible=True)

    def build_document(self, instance):
        return {
            'url': instance.get_absolute_url(),
            'title': instance.title,
            'text': instance.text,
        }
