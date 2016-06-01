"""
    Шаблон поиска по сайту.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'search',
                ...
            )

        urls.py:
            url(r'^search/', include('search.urls', namespace='search')),
"""