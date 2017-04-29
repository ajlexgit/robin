"""
    Добавление в админку урлов на добавление / редактирование / удаление
    сущностей, на основе ContentType.

    Например, вместо "/dladmin/sites/site/1/" можно перейти по адресу
    "/dladmin/ctr/change/6/1/" (будет сделан редирект на первый адрес).
    В некоторых случаях получить URL по ContentType намного проще (например, в JS).

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
