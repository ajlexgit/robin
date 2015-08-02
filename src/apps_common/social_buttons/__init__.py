"""
    Плагин соцкнопок.
    Может получать информацию из Opengraph-модуля.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'social_buttons',
                ...
            )
            MIDDLEWARE_CLASSES = (
                ...
                'opengraph.middleware.OpengraphMiddleware',
                ...
            )

    Пример использования:
        template.html:
            {% load social_buttons %}
            ...
            {% social_share 'vk' image=item.preview.url %}
            {% social_share 'fb' title="Hello" %}
            {% social_share 'tw' title="Hello" description="Test" %}


    # === OAUTH ===
    Установка:
        urls.py:
            ...
            url(r'^social/', include('social_buttons.urls', namespace='social')),
            ...
"""
