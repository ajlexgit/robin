"""
    Плагин соцкнопок.
    Включает соцкнопки "Поделиться", автопостинг в соцсети, виджет Instagram.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'social_networks',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'social_networks',
                    'icon': 'icon-bullhorn',
                    'models': (
                        'FeedPost',
                        'SocialLinks',
                        'SocialConfig',
                    ),
                },
                ...
            }

        urls.py:
            ...
            url(r'^social/', include('social_networks.urls', namespace='social_networks')),
            ...


    Соцкнопки "Поделиться":
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

    Виджет Instagram:
        # Нужно подключить JS и SCSS

        template.html:
            {% load instagram %}

            <!-- Вывод постов юзера -->
            {% instagram_widget user_id=1485581141 limit=6 %}

            <!-- Вывод постов по хэштегу -->
            {% instagram_widget tag="Moscow" limit=6 %}

    Автопостинг:
        Для Google Plus необходимо зарегистрироваться в https://hootsuite.com
        Для остальных соцсетей нужно настроить cron на выполнение
            python3 manage.py autopost

        # crontab
            */15 * * * * . $HOME/.profile; ~/project.com/env/bin/python3 ~/project.com/src/manage.py autopost
            
        admin.py:
            from social_networks.admin import AutoPostMixin
            ...

            class PostAdmin(SeoModelAdminMixin, AutoPostMixin, admin.ModelAdmin):
                ...
                def get_autopost_text(self, obj):
                    return obj.note

"""
default_app_config = 'social_networks.apps.Config'