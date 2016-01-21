"""
    Интернет-магазин с корзиной в localStorage и сессии.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'shop',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'app': 'shop',
                    'icon': 'icon-shopping-cart',
                    'models': (
                        'shoporder',
                        'shopproduct',
                        'shopcategory',
                        'shopconfig',
                    )
                },
                ...
            }

        urls.py:
            ...
            url(r'^shop/', include('shop.urls', namespace='shop')),
            ...

    При конкретной реализации, нужно вызывать Django-сигналы
    для подтверждения, оплаты и отмены заказа:
        from .signals import order_confirmed
        ...
        order_confirmed.send(sender=ShopOrder, order=order, request=request)


"""

default_app_config = 'shop.apps.Config'