"""
    Аналог стандартному тэгу {% cache %}, но может подгружать данные из кэша через AJAX.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.cacheblock',
                ...
            )

            PIPELINE = {
                ...
                'cacheblock/js/cacheblock.js',
                ...
            }

        urls.py:
            ...
            url(r'^cacheblock/', include('libs.cacheblock.urls', namespace='cacheblock')),
            ...

    Необязательные настройки:
        CACHEBLOCK_BACKEND = 'default'

    Для отлова события загрузки всех блоков можно
    использовать событие "loaded.cacheblock":
        $(document).on('loaded.cacheblock', function() {

        })

    Пример:
        Первые два параметра - обязательны.
        Первый - время кэширования (не меньше 120).
        Второй - имя фрагмента в кэше
        Остальные - дополнительные данные для составления ключа кэша

        # template.html:
            {% load cacheblock %}

            {% cacheblock 3600 unique_name ajax=true %}
                ...
            {% endcacheblock %}

"""
default_app_config = 'libs.cacheblock.apps.Config'
