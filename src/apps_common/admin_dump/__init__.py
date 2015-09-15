"""
    Модуль бэкапов данных.

    Установка:
        settings.py:

            INSTALLED_APPS = (
                ...
                'admin_dump',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'icon': 'icon-hdd',
                    'label': 'backups',
                    'url': 'admin_dump:index',
                },
                ...
"""
default_app_config = 'admin_dump.apps.Config'
