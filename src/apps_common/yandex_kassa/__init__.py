"""
    Модуль Яндекс.Кассы для оплаты.

    Взят отсюда и пофиксены баги:
        https://github.com/yandex-money/yandex-money-kit-django

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...,
                'yandex_money',
                ...
            )

            YANDEX_KASSA_SHOP_ID = 56789
            YANDEX_KASSA_SCID = 12345
            YANDEX_KASSA_SHOP_PASSWORD = 'password'
            YANDEX_KASSA_FAIL_URL = 'https://example.com/fail-payment/'
            YANDEX_KASSA_SUCCESS_URL = 'https://example.com/success-payment/'
            # информировать о случаях, когда модуль вернул Яндекс.Кассе ошибку
            YANDEX_KASSA_MAIL_ADMINS_ON_PAYMENT_ERROR = True

        urls.py:
            ...
            url(r'^fail-payment/$', ...),
            url(r'^success-payment/$', ...),
            url(r'^yandex-money/', include('yandex_money.urls')),
            ...

    Использование:
        Модуль работает со своим классом счетов, представленным моделью Payment.
        Если на сайте своя модель счета, то в неё необходимо добавить ссылку на Payment:
            from yandex_money.models import Payment

            class MyOrder(models.Model):
                ...
                payment = models.OneToOneField(Payment, verbose_name=_('payment'))
                ...

        При создании заказа, необходимо также создать объект Payment.
        Назначение полей класса Payment можно подсмотреть тут:
            https://tech.yandex.ru/money/doc/payment-solution/payment-form/payment-form-http-docpage/

        Пример создания заказа собственного класса:
            from uuid import uuid4
            from yandex_money.models import Payment

            myorder = MyOrder()
            myorder.hash = str(uuid4()).replace('-', '')

            payment = Payment(
                order_amount = price,
                order_number = myorder.hash,
                payment_type = 'PC',
            )
            payment.clean()
            payment.save()

            myorder.payment = payment
            myorder.save()

        Для вывода платежной кнопки нужно создать форму PaymentForm:
            views.py:
                from yandex_money.forms import PaymentForm
                payment_form = PaymentForm(instance=myorder.payment)

            template.html:
                <form method="post" action="https://money.yandex.ru/eshop.xml">
                    {{ payment_form.shopId.as_hidden }}
                    {{ payment_form.scid.as_hidden }}
                    {{ payment_form.customerNumber.as_hidden }}
                    {{ payment_form.sum.as_hidden }}

                    <!-- необязательные поля -->
                    {{ payment_form.paymentType.as_hidden }}
                    {{ payment_form.orderNumber.as_hidden }}
                    {{ payment_form.shopFailURL.as_hidden }}
                    {{ payment_form.shopSuccessURL.as_hidden }}

                    <input type="submit" value="Pay">
                </form>

"""