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

"""

default_app_config = 'shop.apps.Config'