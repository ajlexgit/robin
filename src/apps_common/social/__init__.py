"""
    Плагин соцкнопок.
    Может получать информацию из Opengraph-модуля.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'social',
                ...
            )
            MIDDLEWARE_CLASSES = (
                ...
                'social.middleware.OpengraphMiddleware',
                ...
            )

    Пример использования:
        template.html:
            {% load social %}
            ...
            {% social_share 'vk' image=item.preview.url %}
            {% social_share 'fb' title="Hello" %}
            {% social_share 'tw' title="Hello" description="Test" %}
"""