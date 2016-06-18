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
    Либо, можно создать в одном из приложений единый файл indexes.py.

    Пример:
        # indexes.py:
            from libs.sphinx import SphinxScheme, SphinxXMLIndex, ATTR_TYPE
            from .models import Post

            class SearchScheme(SphinxScheme):
                def __init__(self, index_name):
                    super().__init__(index_name)
                    self.add_fields('title', is_attribute=True)
                    self.add_fields('text')
                    self.add_attr('url')
                    self.add_attr('date', ATTR_TYPE.TIMESTAMP)

            class PostIndex(SphinxXMLIndex):
                name = 'news'
                model = Post
                scheme_class = SearchScheme

                def get_queryset(self):
                    return self.model.objects.filter(visible=True)

                def document_dict(self, instance):
                    return {
                        'url': instance.get_absolute_url(),
                        'title': instance.title,
                        'text': instance.text,
                        'date': instance.date,
                    }

        # sphinx.conf:
            source news
            {
                type                    = xmlpipe2
                xmlpipe_command         = wget -O - -q -t 1 http://localhost/sphinx/index/news/skvx8wjq8p81d/
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

            # Для выборки моделей из БД при использовании fetch_models()
            def news_queryset(self, model, ids):
                return model.objects.filter(pk__in=ids).select_related('category')

        resutls = MySearchIndex().fetch_dicts('direct line')
"""

from .search import SphinxSearch, SphinxSearchResult
from .index import ATTR_TYPE, SphinxScheme, SphinxXMLIndex

default_app_config = 'libs.sphinx.apps.Config'