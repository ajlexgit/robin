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
            <div class="social-buttons">
                <div class="social-button social-vk">Share</div>
                <div class="social-button social-fb">Share</div>
                <div class="social-button social-gp">Share</div>
                <div class="social-button social-tw">Share</div>
                <div class="social-button social-li">Share</div>
                <div class="social-button social-pn">Share</div>
            </div>
"""
