"""
    Аналог стандартному тэгу {% cache %}, но подгружает данные из кэша через AJAX.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.ajax_cache',
                ...
            )

            PIPELINE = {
                ...
                'ajax_cache/js/ajax_cache.js',
                ...
            }

        urls.py:
            ...
            url(r'^ajax_cache/', include('libs.ajax_cache.urls', namespace='ajax_cache')),
            ...

        Пример:
            Первые два параметра - обязательны.
            Первый - время кэширования (не меньше 120).
            Второй - имя фрагмента в кэше
            Остальные - дополнительные данные для составления ключа кэша

            template.html:
                {% load ajaxcache %}

                {% ajaxcache 3600 unique_name %}
                ...
                {% endajaxcache %}

"""
default_app_config = 'libs.ajax_cache.apps.Config'
