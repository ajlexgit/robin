from libs.sphinx import SphinxXMLIndex, ATTR_TYPE
from blog.models import BlogPost


class BlogPostIndex(SphinxXMLIndex):
    name = 'blog'
    model = BlogPost

    def __init__(self):
        super().__init__()
        self.add_fields('title', is_attribute=True)
        self.add_fields('text')
        self.add_attr('url')
        self.add_attr('date', ATTR_TYPE.TIMESTAMP)

    def get_queryset(self):
        return self.model.objects.filter(visible=True)

    def document_dict(self, instance):
        return {
            'url': instance.get_absolute_url(),
            'title': instance.header,
            'text': instance.text,
            'date': int(instance.date.timestamp()),
        }
