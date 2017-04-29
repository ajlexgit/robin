"""
    Модуль пользовательской карты сайта.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'sitemap',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'sitemap',
                    'icon': 'icon-file',
                },
                ...
            }

        urls.py:
            ...
            url(r'^sitemap/', include('sitemap.urls', namespace='sitemap')),
            ...

    Использование:
        # views.py:

            def _build_map(self):
                sitemap = Map()

                news = Post.objects.all()
                if news.exists():
                    news_page = sitemap.add_child(NewsModule.objects.first())
                    news_page.add_childs(news)
"""

default_app_config = 'sitemap.apps.Config'
