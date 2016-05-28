"""
    Баннер в Popup-окне, появляющийся после заданного времени.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'popup_banner',
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
                'popup_banner.middleware.PopupBannerMiddleware',
                ...
            )

        urls.py:
            ...
            url(r'^popup_banner/', include('popup_banner.urls', namespace='popup_banner')),
            ...

"""
default_app_config = 'popup_banner.apps.Config'