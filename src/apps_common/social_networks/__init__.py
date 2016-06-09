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

            # API для автопостинга
            TWITTER_APP_ID = 'j3tkGKGYdUvJy5i97us36UEaF'
            TWITTER_SECRET = '5xdxDZeQQi8mUjpQ86rtr2dMZqkSOn4wQFP4VPNlVDGGPhYV51'
            TWITTER_TOKEN = '201200112-g53dkoQAgJCYxgpiMw4AMpeM8QOuyXrvm5VAh7Cu'
            TWITTER_TOKEN_SECRET = '37Hc33tE6cBHIDEDEwQFaMFwPsCf3mXQABuXKuKsZiVI7'
            FACEBOOK_APP_ID = '248477118860039'
            FACEBOOK_SECRET = 'de160348bca3aac4598d2246e6e4f7cb'
            FACEBOOK_TOKEN = 'EAADhZCRZAniwcBACypvz4YG5bszBRRPfA5IdDdFEZCHYvYbPQshumfUZCPhY' \
                             'MZC2OlDOM3JE32h85p0ZApw56L87ZAz5OYwvZBkhsQMQoNItj0B7bHxnMZAZB' \
                             'ggD2fZCB0tpmMjOcVct9YCS3NIYwvSWLwpxoLC0aypj8wGf6B9LLaLyQIZBoZ' \
                             'BZCTWft9TfHZBk0KlUvbu2O5SQ7z8jOH2DMd5BEo4'

        urls.py:
            ...
            url(r'^social/', include('social_networks.urls', namespace='social_networks')),
            ...


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


    Автопостинг:
        Для Google Plus необходимо зарегистрироваться в https://hootsuite.com
        Для остальных соцсетей нужно настроить cron на выполнение
            python3 manage.py autopost

    # ==============================================

    Токен для Facebook имеет максимальное время жизни 2 месяца.
    Он автоматически продлевается при вызове autopost. Если токен не обновлялся
    более 2-х месяцев, нужно создавать его заново.
        https://developers.facebook.com/tools/explorer/


"""
from .rss import SocialRssFeed

default_app_config = 'social_networks.apps.Config'