"""
    Всплывающий баннер.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'facebook_banner',
                ...
            )

        urls.py:
            ...
            url(r'^facebook_banner/', include('facebook_banner.urls', namespace='facebook_banner')),
            ...

"""
default_app_config = 'facebook_banner.apps.Config'