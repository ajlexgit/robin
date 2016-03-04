"""
    Модуль оплаты через Gotobilling.

    http://www.gotobilling.com/wiki/index.php?title=One_Click
    http://www.gotobilling.com/wiki/index.php?title=Advanced_Integration_Method

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'gotobilling',
                ...
            )

            GOTOBILLING_MID = 122879
            GOTOBILLING_HASH = 'myShop123'
            GOTOBILLING_SUCCESS_REDIRECT_URL = 'shop:index'
            GOTOBILLING_FAIL_REDIRECT_URL = 'shop:index'

            SUIT_CONFIG = {
                ...
                {
                    'app': 'gotobilling',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'log',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^gotobilling/', include('gotobilling.urls', namespace='gotobilling')),
            ...

    Настройки (settings.py):
        # ID магазина
        GOTOBILLING_MID = 122879

        # Gateway Hash
        GOTOBILLING_HASH = 'myShop123'

        # Адрес страницы, куда перенаправит пользователя
        # после успешной оплаты
        GOTOBILLING_SUCCESS_REDIRECT_URL = 'shop:index'

        # Адрес страницы, куда перенаправит пользователя
        # после неудачной оплаты
        GOTOBILLING_FAIL_REDIRECT_URL = 'shop:index'

    Пример:
        views.py:
            from gotobilling.forms import GotobillingForm
            ...

            gotobilling_form = GotobillingForm(initial={
                'x_invoice_num': 1,
                'x_amount': 12.5,
                'x_description': 'Золотое кольцо',
                'x_relay_url': request.build_absolute_uri(resolve_url('gotobilling:result')),
            })
            ...


            @receiver(gotobilling_success)
            def gotobilling_success_handler(sender, **kwargs):
                inv_id = kwargs['inv_id']
                request = kwargs['request']

            @receiver(gotobilling_error)
            def gotobilling_error_handler(sender, **kwargs):
                inv_id = kwargs['inv_id']
                request = kwargs['request']
                code = kwargs['code']
                reason = kwargs['reason']

        template.html:
            <form action="{{ gotobilling_form.target }}" method="post">
              {{ gotobilling_form.as_p }}
              <button type="submit">Pay</button>
            </form>

"""

default_app_config = 'gotobilling.apps.Config'
