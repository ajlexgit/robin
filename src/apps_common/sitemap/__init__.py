"""
    Модуль пользовательской карты сайта.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'sitemap',
                ...
            )

        urls.py:
            ...
            url(r'^sitemap/', include('sitemap.urls', namespace='sitemap')),
            ...
"""

default_app_config = 'sitemap.apps.Config'