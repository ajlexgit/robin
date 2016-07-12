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
                    ),
                },
                ...
            }

            # API для автопостинга
            TWITTER_APP_ID = 'j3tkGKGYdUvJy5i97us36UEaF'
            TWITTER_SECRET = '5xdxDZeQQi8mUjpQ86rtr2dMZqkSOn4wQFP4VPNlVDGGPhYV51'
            TWITTER_TOKEN = '201200112-g53dkoQAgJCYxgpiMw4AMpeM8QOuyXrvm5VAh7Cu'
            TWITTER_TOKEN_SECRET = '37Hc33tE6cBHIDEDEwQFaMFwPsCf3mXQABuXKuKsZiVI7'
            FACEBOOK_TOKEN = 'EAADhZCRZAniwcBAONB6fBjEgG0vZAJCRir46Lpa02Yb0aOtoA8FI' \
                             'DMXOL7sJxLxptZCi7pkkC1XUi1uVIkjqZArCARcgx8ZCtKA7qw8Vm' \
                             '9C6IIKqOoOE8RTYnVigifVirZBwID4OUTZB6dyI1mVDwfimIJjZCy' \
                             'juf2diToFYsVClwYQZDZD'
            LINKEDIN_TOKEN = 'AQVDPMVg20HqmE0bJWq9pm27iFe116GKlrH9o7vHu_Xp1O89ySf0i' \
                             'lw3GZc4W_u4zNI0EUD9EfnedLfAiEJxSmansU_P6eDPU5Pq8oJ-33' \
                             'qDg_GxHw-Yi7C5DzunRuV_ab5fQxZRN8elsuukWx29kl_B-yamd4g' \
                             'OH8nHA-Uv5FESS7Ul2MM'

            # Виджет Instagram
            INSTAGRAM_TOKEN = '481470271.0a39b8a.872bb1e18c044e6fbadf88b9a422970b'

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

            {% instagram_widget user_id=1485581141 limit=6 %}

    Автопостинг:
        Для Google Plus необходимо зарегистрироваться в https://hootsuite.com
        Для остальных соцсетей нужно настроить cron на выполнение
            python3 manage.py autopost

        admin.py:
            from social_networks.admin import AutoPostMixin
            ...

            class PostAdmin(SeoModelAdminMixin, AutoPostMixin, admin.ModelAdmin):
                ...
                def get_autopost_text(self, obj):
                    return obj.note

"""
from .rss import SocialRssFeed
from .utils import post_to_twitter, post_to_facebook, post_to_linkedin

default_app_config = 'social_networks.apps.Config'