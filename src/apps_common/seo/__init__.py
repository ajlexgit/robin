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
    
    Пример:
        template.html:
            ...
            <title>{{ seo.title }}</title>
            <meta name="keywords" content="{{ seo.keywords }}" />
            <meta name="description" content="{{ seo.description }}" />
            ...
"""