"""
    Добавление в админку урлов на добавление / редактирование / удаление
    сущностей, на основе ContentType.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'admin_ctr',
                ...
            )

        urls.py:
            ...
            url(r'^dladmin/ctr/', include('admin_ctr.urls', namespace='admin_ctr')),
            ...

"""
default_app_config = 'admin_ctr.apps.Config'