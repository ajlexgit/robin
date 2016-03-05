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
            gotobilling_form = GotobillingForm(
                request,
                initial={
                    'x_invoice_num': 1,
                    'x_amount': '12.50',
                    'x_description': 'Золотое кольцо',
                }
            )
            ...


            @receiver(gotobilling_success)
            def payment_success(sender, **kwargs):
                inv_id = kwargs['inv_id']
                request = kwargs['request']

            @receiver(gotobilling_error)
            def payment_error(sender, **kwargs):
                inv_id = kwargs['inv_id']
                request = kwargs['request']
                code = kwargs['code']
                reason = kwargs['reason']

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form.as_p }}
              <button type="submit">Pay</button>
            </form>

"""
from .forms import GotobillingForm
from .signals import gotobilling_success, gotobilling_error

default_app_config = 'gotobilling.apps.Config'
