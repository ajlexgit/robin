"""
    Шаблон поиска по сайту.

    Зависит от:
        libs.sphinx

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