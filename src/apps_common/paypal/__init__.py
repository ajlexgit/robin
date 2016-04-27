"""
    Модуль оплаты через PayPal.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'paypal',
                ...
            )

            PAYPAL_EMAIL = 'pix666-facilitator@ya.ru'
            PAYPAL_SUCCESS_URL = 'shop:index'
            PAYPAL_CANCEL_URL = 'shop:index'

            SUIT_CONFIG = {
                ...
                {
                    'app': 'paypal',
                    'icon': 'icon-shopping-cart',
                },
                ...
            }

        urls.py:
            ...
            url(r'^paypal/', include('paypal.urls', namespace='paypal')),
            ...

    Настройки (settings.py):
        # E-mail аккаунта магазина
        PAYPAL_EMAIL = 'pix666-facilitator@ya.ru'

        # Адреса для редиректа юзера
        PAYPAL_SUCCESS_URL = 'shop:index'
        PAYPAL_CANCEL_URL = 'shop:index'

        # Код валюты
        PAYPAL_CURRENCY = 'RUB'

        # тестовый режим
        PAYPAL_TEST_MODE = False

    Пример:
        views.py:
            from paypal import *

            ...
            # форма мгновенной оплаты
            form = PaymentForm(request, initial={
                'invoice': 18,
                'amount': '12.50',
                'description': 'Золотое кольцо',
                'quantity': 2,      // 2 штуки
            })

            # форма добавления товара в корзину
            add_cart_form = AddToCartForm(request, initial={
                'invoice': 18,
                'amount': '12.50',
                'description': 'Золотое кольцо',
                'quantity': 2,      // 2 штуки
            })

            # форма для просмотра корзины
            display_cart_form = DisplayCartForm(request, initial={
                'invoice': 18,
            })

            # форма для пожертвований
            donate_form = DonationForm(request, initial={
                'amount': '10.00',
                'description': 'На еду',
            })


            # можно сразу перенаправить
            return redirect(form.get_redirect_url())
            ...


            @receiver(paypal_success)
            def payment_success(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']

            @receiver(paypal_error)
            def payment_error(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']
                code = kwargs['code']
                reason = kwargs['reason']

        template.html:
            <form action="{{ form.target }}" method="post">
              {{ form.as_p }}
              <button type="submit">Pay</button>
            </form>

"""
from .forms import PaymentForm, AddToCartForm, DisplayCartForm, DonationForm
from .signals import paypal_success, paypal_error

default_app_config = 'paypal.apps.Config'

__all__ = ('PaymentForm', 'AddToCartForm', 'DisplayCartForm', 'DonationForm',
           'paypal_success', 'paypal_error')