"""
    СЕО-модуль.

    Установка:
        settings.py:
            MIDDLEWARE_CLASSES = (
                ...
                'seo.middleware.SeoMiddleware',
                ...
            )

            TEMPLATE_CONTEXT_PROCESSORS = (
                ...
                'seo.context_processors.seo',
                ...
            )

    Настройки:
        settings.py:
            SEO_TITLE_JOIN_WITH = ''

    Пример:
        views.py:
            ...
            request.seo.set(title='Clients')
            ...

        template.html:
            ...
            <title>{{ seo.title }}</title>
            <meta name="keywords" content="{{ seo.keywords }}" />
            <meta name="description" content="{{ seo.description }}" />
            ...
"""
default_app_config = 'seo.apps.Config'