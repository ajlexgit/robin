"""
    Всплывающий баннер.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'popup_banner',
                ...
            )

            MIDDLEWARE_CLASSES = (
                ...
                'popup_banner.middleware.BannerMiddleware',
                ...
            )

        urls.py:
            ...
            url(r'^popup_banner/', include('popup_banner.urls', namespace='popup_banner')),
            ...

"""
default_app_config = 'popup_banner.apps.Config'