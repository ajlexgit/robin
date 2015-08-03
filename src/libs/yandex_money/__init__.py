"""
    Плагин кассы Яндекса.

    Документация:
        https://money.yandex.ru/i/forms/guide-to-custom-p2p-forms.pdf

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.yandex_money',
                ...
            )

    Настройки:
        YANDEX_MONEY_WALLET = '41001984822868'
        # Номер кошелька-получателя

        YANDEX_MONEY_SECRET = '4FOx8cth9Rqd7CT7AV4HBLES'
        # Секретный ключ для валидации

        YANDEX_MONEY_DEFAULT_DESCRIPTION = _('Evolut')
        # Название платежей о умолчанию

        YANDEX_MONEY_DEFAULT_TARGETS = _('Transaction')
        # Описание платежей по умолчанию

    Пример использования:
        template.html:
            <form method="post" action="{% yandex_money_url %}" target="_blank">
                {% yandex_money amount=0.5 payment_type='PC' label=order.hash description='My payment' targets='transaction 1' %}

                <button>{% trans 'Pay' %}</button>
            </form>

        views.py:
            # Валидация:
            from libs.yandex_money.validation import validate, InvalidPaymentRequest

            def payment_callback(request):
                ...

                try:
                    payment = validate(request)
                except InvalidPaymentRequest:
                    raise Http404

                ...
"""
