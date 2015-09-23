"""
    Модуль, отвечающий за кэширование.

    1) Декоратор кэширования функций и методов "cached",
       использующий для составления ключа значения параметров функции.

       Поддерживает указание атрибутов параметров, например "request.city.id".
       Данная нотация может быть использована и для свойств и для индексов (dectionary.index).

       Параметры:
           cache_time      - время кэширования в секундах
           key             - список/кортеж имен параметров функции, которые
                             будут использованы для составления ключа кэша
           key_const       - список/кортеж дополнительных значений, которые будут использованы
                             для составления ключа кэша
           backend         - идентификатор используемого бэкенда кэширования

       Пример использования:
           @cached(['title', 'address.street', 'addition.key'], [settings.CACHE_VERSION], time=3600)
           def MyFunc(title, address, addition={'key': 1})
               ...
               return ...

    2) Middleware, автоматически проставляющая заголовки cache-control.
       Создана на базе https://github.com/koalalorenzo/django-smartcc.

       Если юзер авторизован, то ставятся заголовки
         Cache-control: private, max-age=0
       если не авторизован, то:
         Cache-control: public, max-age=43200

        Установка:
            settings.py:
                MIDDLEWARE_CLASSES = (
                    ...
                    'libs.cache.middleware.SCCMiddleware',
                    ...
                )

                # Пользовательские правила
                SCC_CUSTOM_CACHE_CONTROLS = [
                    # не кэшировать ВСЁ, что начитнается с /users/
                    (r'^/users/', 'no-cache', 0),

                    # кэшировать главную магазина на 5м
                    (r'^/shop/$', 'public', 600),
                ]

"""

from .cached import cached

__all__ = ['cached']