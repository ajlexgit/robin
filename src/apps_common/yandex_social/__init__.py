"""
    Плагин соцкнопок Яндекс.Поделиться.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'yandex_social',
                ...
            )

    Требуется подключить:
        yandex_social/js/social.js

    Настройки:
        SOCIAL_BUTTONS_DEFAULT = ('vkontakte', 'facebook', 'twitter', 'gplus')
        # Полный список - https://tech.yandex.ru/share/doc/dg/concepts/share-button-ov-docpage/#supported-networks

        SOCIAL_BUTTON_TYPE_DEFAULT = 'button'
        # Полный список - https://tech.yandex.ru/share/doc/dg/concepts/share-button-ov-docpage/#params.elementStyle.type

        SOCIAL_BUTTON_THEME_DEFAULT = 'counter'
        # Полный список - https://tech.yandex.ru/share/doc/dg/concepts/share-button-ov-docpage/#params.l10n_1

    Пример использования:
        views.py:
            from yandex_social import social_buttons
            from libs.description import description
            from django.utils.html import strip_tags
            ...
                # Настройки соцкнопок
                social_settings = {
                    'url': request.build_absolute_uri(),
                    'title': post.title,
                    'description': description(strip_tags(post.text), 50, 150),
                }
                if post.preview:
                    social_settings['image'] = request.build_absolute_uri(post.preview.url)

                # Opengraph
                request.opengraph.update(social_settings)

                context = {
                    ...
                    'social_buttons': social_buttons(social_settings),
                    ...
                }

        template.html:
            ...
            {{ yandex_social_buttons }}
            ...

    Обновление блока через AJAX:
        $('.yandex_social-buttons').socialButtons('update', {
            url: 'http://example.com/page/1/',
            title: 'test',
            description: 'Hello',
            image: 'http://example.com/1.jpg'
        })
"""

from .social import social_buttons

__all__ = ['social_buttons']