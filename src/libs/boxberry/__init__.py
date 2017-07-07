"""
    API сервиса BOXBERRY.

    http://boxberry.ru/upload/iblock/50d/web-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B%20Boxberry.pdf

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                # если нужен доступ через JS
                'libs.boxberry',
                ...
            )

            # тестовый режим
            BOXBERRY_TEST = False

            # токен тестового режима
            BOXBERRY_API_TEST_TOKEN = '31705.rvpqcbfd'

            # токен реального режима
            BOXBERRY_API_TOKEN = '12345.abcdefgh'

    Пример:
        ...
"""

default_app_config = 'libs.boxberry.apps.Config'
