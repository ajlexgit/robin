"""
    Модуль бэкапов данных.

    Зависит от:
        libs.download

    Установка:
        settings.py:

            INSTALLED_APPS = (
                ...
                'backups',
                ...
            )

            SUIT_CONFIG = {
                ...
                {
                    'icon': 'icon-hdd',
                    'label': 'backups',
                    'url': 'backups:index',
                },
                ...
            }

            BACKUP_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'backup'))

        urls.py:
            ...
            url(r'^dladmin/dump/', include('backups.admin_urls', namespace='backups')),
            ...

"""

default_app_config = 'backups.apps.Config'