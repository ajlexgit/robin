"""
    Плагин соцкнопок.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'social_buttons',
                ...
            )

    Пример использования:
        template.html:
            {% load social_buttons %}

            <div class="social-buttons no-counter">
              {% social_button 'vk' %}
              {% social_button 'fb' %}
              {% social_button 'tw' %}
              {% social_button 'gp' %}
              {% social_button 'li' %}
              {% social_button 'pn' %}
            </div>
"""
