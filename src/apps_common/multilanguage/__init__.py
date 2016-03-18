"""
    Средства поддержки разноязычных версий сайта.

    Зависит от:
        libs.geocity

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'multilanguage',
                ...
            )

            MIDDLEWARE_CLASSES = (
                ...
                'multilanguage.middleware.LanguageRedirectMiddleware',
                ...
            )

        urls.py:
            ...
            url(r'^langs/', include('multilanguage.urls', namespace='multilanguage')),
            ...

        В options.py должны быть указаны поддерживаемые языки и их URL. Коды языков должны
        совпадать с кодами в settings.LANGUAGE_CODE на указанных сайтах:
            LANGUAGES = {
                'en': {
                    'url': '//mysite.com/',
                },
                'ru': {
                    'url': '//mysite.ru/',
                    'iso': ('RU', 'UA'),
                },
            }

    Примеры:
        template.html:
            <!-- Блок выбора языка -->
            {% load multilanguage %}

            ...
                <div>
                    {% select_language %}
                </div>
            ...
"""
