"""
    Модуль оплаты через Robokassa.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'robokassa',
                ...
            )

            ROBOKASSA_LOGIN = 'asskicker'
            ROBOKASSA_PASSWORD1 = 'hachapuri666'
            ROBOKASSA_PASSWORD2 = 'bublik72x'
            ROBOKASSA_SUCCESS_REDIRECT_URL = 'shop:index'
            ROBOKASSA_FAIL_REDIRECT_URL = 'shop:index'
            ROBOKASSA_TEST_MODE = True

            SUIT_CONFIG = {
                ...
                {
                    'app': 'robokassa',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'log',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^robokassa/', include('robokassa.urls', namespace='robokassa')),
            ...

    Настройки (settings.py):
        # Логин магазина
        ROBOKASSA_LOGIN = 'super_shop'

        # Первый пароль магазина
        ROBOKASSA_PASSWORD1 = 'a123b5c6h'

        # Второй пароль магазина
        ROBOKASSA_PASSWORD2 = 'nkvo6s8bv'

        # Адрес страницы, куда перенаправит пользователя
        # после успешной оплаты
        ROBOKASSA_SUCCESS_REDIRECT_URL = 'shop:index'

        # Адрес страницы, куда перенаправит пользователя
        # после неудачной оплаты
        ROBOKASSA_FAIL_REDIRECT_URL = 'shop:index'

        # === Не обязательные ===

        # Использовать метод POST для уведомлений
        ROBOKASSA_USE_POST = True

        # Требовать наличия уведомления ResultURL перед SuccessURL
        ROBOKASSA_STRICT_CHECK = True

        # Тестовый режим магазина
        ROBOKASSA_TEST_MODE = False

        # Дополнительные данные уведомлений
        ROBOKASSA_EXTRA_PARAMS = ['shp_param1', 'shp_param2']

    Примеры:

        views.py:
            from robokassa.forms import RobokassaForm
            ...

            robokassa_form = RobokassaForm(initial={
                'InvId': 1,
                'OutSum': 12.5,
                'Desc': 'Золотое кольцо',
            })
            ...

            @receiver(robokassa_paid)
            def robokassa_paid_handler(sender, **kwargs):
                inv_id = kwargs['inv_id']
                out_sum = kwargs['out_sum']
                extra = kwargs['extra']

        template.html:
            <form action="{{ robokassa_form.target }}" method="post">
              {{ robokassa_form.as_p }}
              <button type="submit">Pay</button>
            </form>

"""

# TODO: donut form
default_app_config = 'robokassa.apps.Config'
