"""
    Модуль промокодов для заказов.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'promocodes',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'promocodes',
                    'models': (
                        'PromoCode',
                    )
                },
                ...
            }

    Детали реализации:
        Промокод - текстовый код, вводимый заказчиком при оформлении заказа.
        У каждого промокода есть стратегия (паттерн), которая по объекту заказа
        вычисляет размер скидки.

        Промокод может быть ограничен по времени и/или по количеству использований.
        При каждом использовании промокода нужно вызывать метод PromoCode.add_order():
            from promocodes.exceptions import PromoCodeError

            try:
                promocode.add_order(order)
            except PromoCodeError as e:
                ...

        Этот метод создает связь промокода с заказом и тем самым увеличит счётчик кол-ва использований промокода.
        !!! ВНИМАНИЕ !!! Этот метод может генерировать исключения из promocodes.exceptions


        Для получения всех промокодов нужно вызвать функцию:
            promocodes.utils.get_promocodes(order)

        Она вернёт кортеж объектов PromoCode с дополнительным полем calculated_discount,
        хранящим рассчитанную для заказа скидку в формате Valute.

"""
default_app_config = 'promocodes.apps.Config'
