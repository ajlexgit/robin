"""
    Модуль оплаты через Authorize.NET.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'authorize_net',
                ...
            )

            AUTHORIZENET_TEST_MODE = False
            AUTHORIZENET_LOGIN_ID = '9cE66cSQ'
            AUTHORIZENET_MD5_HASH = 'prestige'
            AUTHORIZENET_TRANSACTION_KEY = '69y7xQ999duHGE8v'

            AUTHORIZENET_SEQUENCE = '1856512237'
            AUTHORIZENET_SUCCESS_URL = 'shop:index'
            AUTHORIZENET_RECEIPT_URL = 'shop:index'

            SUIT_CONFIG = {
                ...
                {
                    'app': 'authorize_net',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'log',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^authorize_net/', include('authorize_net.urls', namespace='authorize_net')),
            ...

    Настройки (settings.py):
        # Login ID
        AUTHORIZENET_LOGIN_ID = '9cE66cSQ'

        # Transaction Key
        AUTHORIZENET_TRANSACTION_KEY = '69y7xQ999duHGE8v'

        # MD5 Hash
        AUTHORIZENET_MD5_HASH = 'prestige'

        # Рандомно сгенерированная числовая последовательность
        AUTHORIZENET_SEQUENCE = '1856512237'

        # Адрес страницы, куда перенаправит пользователя
        # при отмене оплаты
        AUTHORIZENET_CANCEL_URL = 'shop:index'

        # Адрес ссылки возврата на сайт со страницы квитанции
        AUTHORIZENET_RECEIPT_URL = 'shop:index'

    Пример:
        views.py:
            from authorize_net import *

            ...
            form = PaymentForm(request, initial={
                'invoice': 1,
                'amount': '12.50',
                'description': 'Золотое кольцо',
            })

            # можно сразу перенаправить
            return redirect(form.get_redirect_url())
            ...


            @receiver(authorizenet_success)
            def payment_success(sender, **kwargs):
                invoice = kwargs['invoice']
                request = kwargs['request']

            @receiver(authorizenet_error)
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
from .forms import PaymentForm
from .signals import authorizenet_success, authorizenet_error

default_app_config = 'authorize_net.apps.Config'

__all__ = ('PaymentForm', 'authorizenet_success', 'authorizenet_error')