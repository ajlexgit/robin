from .modules.profiler import devprofile, devprofiler

__all__ = ('devprofile', 'devprofiler')

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
        from devserver import devprofile
        
        @devprofile
        def get(self, request, post_id):
            ...
    
    Профилирование участков кода:
        from devserver import devprofiler
        
        with devprofiler('entity fetch'):
            e = Entity.objects.get(pk=1)
"""