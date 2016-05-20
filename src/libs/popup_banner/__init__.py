"""
    Всплывающий баннер.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.popup_banner',
                ...
            )

            SUIT_CONFIG = (
                ...
                {
                    'app': 'popup_banner',
                },
                ...
            )

            MIDDLEWARE_CLASSES = (
                ...
                'libs.popup_banner.middleware.PopupBannerMiddleware',
                ...
            )

        urls.py:
            ...
            url(r'^popup_banner/', include('libs.popup_banner.urls', namespace='popup_banner')),
            ...

"""
default_app_config = 'libs.popup_banner.apps.Config'