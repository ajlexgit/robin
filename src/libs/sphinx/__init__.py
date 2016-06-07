"""
    Модуль поиска через Sphinx.

    Установка:
        settings.py:
            INSTALLED_APS = (
                ...
                'libs.sphinx',
                ...
            )

        urls.py:
            ...
            url(r'^sphinx/', include('libs.sphinx.urls', namespace='sphinx')),
            ...

    В каждом индексируемом приложении должен быть файл с опрелением индексов indexes.py.

    Пример индексации:
        indexes.py:
            from django.utils.html import strip_tags
            from libs.sphinx import SphinxXMLIndex, ATTR_TYPE
            from .models import Post

            class PostIndex(SphinxXMLIndex):
                name = 'news'
                model = Post

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
                        'title': instance.title,
                        'text': strip_tags(instance.text),
                        'date': int(instance.date.timestamp()),
                    }

        sphinx.conf:
            source news
            {
                type                    = xmlpipe2
                xmlpipe_command         = curl --connect-timeout 3 http://localhost/sphinx/index/news/skvx8wjq8p81d/
            }
            
            index news
            {
                source              = news
                path                = C:/sphinx/data/index/news
                morphology          = stem_en
                min_stemming_len    = 4
                min_word_len        = 3
                min_prefix_len      = 3
                index_exact_words   = 1
                expand_keywords     = 1
                html_strip          = 1
            }


    Пример поиска:
        from libs.sphinx import SphinxSearch

        class MySphinxSearch(SphinxSearch):
            limit = 20
            weights = {
                'title': 2,
                'text': 1,
            }

            def news_queryset(self, model, ids):
                return model.objects.filter(pk__in=ids).select_related('category')

        queryset = MySearchIndex().fetch_models('direct line')

"""

from .search import SphinxSearch, SphinxSearchResult
from .index import ATTR_TYPE, SphinxXMLIndex

default_app_config = 'libs.sphinx.apps.Config'