"""
    Средства поддержки разноязычных версий сайта.

    Зависит от:
        libs.geocity

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'multilanguage',
                'libs.geocity',
                ...
            )

            MIDDLEWARE_CLASSES = (
                ...
                'multilanguage.middleware.LanguageRedirectMiddleware',
                ...
            )

            # Для поиска языковых шаблонов (опционально) можно использовать
            # один из специальных загрузчиков:
            #   1) multilanguage.loaders.LanguageLoader
            #   2) multilanguage.loaders.LanguageCachedLoader
            TEMPLATE = {
                ...
                'OPTIONS': {
                    'loaders': (
                        ('multilanguage.loaders.LanguageCachedLoader', [
                            'django.template.loaders.filesystem.Loader',
                            'django.template.loaders.app_directories.Loader',
                        ]),
                    ),
                }
            }

        urls.py:
            ...
            url(r'^langs/', include('multilanguage.urls', namespace='multilanguage')),
            ...


    Настройки:
        # Ключи словаря должны соответсвовать аналогичным кодам из settings.LANGUAGES
        MULTILANGUAGE_SITES = {
            'en': {
                'url': '//mysite.com/',
            },
            'ru': {
                'url': '//mysite.ru/',
                'iso': ('RU', 'UA'),
            },
        }

        # == Не обязательные ==

        # Запасной URL при авторедиректе. Например, когда на русской версии сайта
        # нет страницы, с которой был совершен редирект.
        MULTILANGUAGE_FALLBACK_URL = 'index'

        # имя куки, хранящей флаг того, что редиректить автоматически с данного сайта не нужно
        MULTILANGUAGE_COOKIE_NAME = 'no_redirect'

        # Имя GET-параметра, запрещающего авторедирект
        MULTILANGUAGE_GET_PARAM = 'no_redirect'

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
