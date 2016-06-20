"""
    Аналог стандартному тэгу {% cache %}, но подгружает данные из кэша через AJAX.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.ajaxcache',
                ...
            )

            PIPELINE = {
                ...
                'ajaxcache/js/ajaxcache.js',
                ...
            }

        urls.py:
            ...
            url(r'^ajaxcache/', include('libs.ajaxcache.urls', namespace='ajaxcache')),
            ...

    Необязательные настройки:
        AJAXCACHE_BACKEND = 'default'

    Для отлова события загрузки всех блоков можно
    использовать событие "ready.ajaxcache":
        $(document).on('ready.ajaxcache', function() {

        })

    Пример:
        Первые два параметра - обязательны.
        Первый - время кэширования (не меньше 120).
        Второй - имя фрагмента в кэше
        Остальные - дополнительные данные для составления ключа кэша

        # template.html:
            {% load ajaxcache %}

            {% ajaxcache 3600 unique_name %}
                ...
            {% endajaxcache %}

"""
default_app_config = 'libs.ajaxcache.apps.Config'