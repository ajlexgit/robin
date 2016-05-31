from haystack import indexes
from .models import BlogPost


class BlogPostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return BlogPost

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(visible=True)
