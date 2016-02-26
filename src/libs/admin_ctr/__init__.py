"""
    Добавление в админку урлов на добавление / редактирование / удаление
    сущностей, на основе ContentType.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.admin_ctr',
                ...
            )

        urls.py:
            ...
            url(r'^dladmin/ctr/', include('libs.admin_ctr.urls', namespace='admin_ctr')),
            ...

"""