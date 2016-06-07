"""
    Плагин соцкнопок.
    Включает кнопки для расшаривания и автопостинг.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'social_networks',
                ...
            )

    Пример вывода кнопок для расшаривания:
        # Нужно подключить JS и SCSS

        template.html:
            {% load social_networks %}

            <div class="social-buttons no-counter">
              {% social_button 'vk' %}
              {% social_button 'fb' %}
              {% social_button 'tw' %}
              {% social_button 'gp' %}
              {% social_button 'li' %}
              {% social_button 'pn' %}
            </div>
"""
