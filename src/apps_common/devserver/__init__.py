"""
    Кастомный сервер для разработки.

    Установка:
        INSTALLED_APPS = (
            'devserver',
            ...
        )

        MIDDLEWARE_CLASSES = (
            ...
            'devserver.middleware.DevServerMiddleware',
        )

    Настройки:
        DEVSERVER_MODULES = (...)
        DEVSERVER_IGNORED_PREFIXES = (
            settings.STATIC_URL,
            settings.MEDIA_URL,
            '/favicon',
        )
        DEVSERVER_SQL_MIN_DURATION = None


    Профилирование функций:
        from devserver import devprofile_func

        @devprofile_func
        def get(self, request, post_id):
            ...

    Профилирование участков кода:
        from devserver import devprofile

        with devprofile('entity fetch', summary=True):
            e = Entity.objects.get(pk=1)
"""
from .modules.profiler import devprofile, devprofile_func

__all__ = ('devprofile', 'devprofile_func')