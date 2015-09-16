"""
    Модуль бэкапов данных.

    Зависит от:
        libs.download

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
            }

            BACKUP_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'backup'))
"""

default_app_config = 'admin_dump.apps.Config'