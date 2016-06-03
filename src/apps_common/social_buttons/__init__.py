"""
    Плагин соцкнопок.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'social_buttons',
                ...
            )

    Получение данных по приоритетам:
        1) data-аттрибут кнопки
        2) data-аттрибут родителя кнопки
        3) Opengraph-тэги
        4) данные на странице (<title>, location.href, ...)

    Возможные аттрибуты:
        data-url
        data-title
        data-image
        data-description

    Пример использования:
        template.html:
            ...
            <div class="social-buttons no-counter">
                <div class="social-button social-vk"></div>
                <div class="social-button social-fb"></div>
                <div class="social-button social-gp"></div>
                <div class="social-button social-tw"></div>
                <div class="social-button social-li"></div>
                <div class="social-button social-pn"></div>
            </div>
"""
