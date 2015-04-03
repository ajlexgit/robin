"""
Определение категории разрешения экрана. 
Список категорий разрешений находится в options.py.

Установка:
    settings.py:
        INSTALLED_APPS = (
            ...
            'libs.resolution',
            ...
        )
        
        MIDDLEWARE_CLASSES = (
            ...
            'libs.js_storage.middleware.JSStorageMiddleware',
            ...
            'libs.resolution.middleware.ResolutionMiddleware',
            ...
        )


Необходимо подключить скрипт:
    resolution/js/resolution.js
    
    
Пример использования:
    views.py:
        request.resolution - ID категории разрешения пользователя.
    
    Javascript:
        $.cookie('resolution') - ID категории разрешения пользователя.
        
        $(document).on('change_resolution', function(old_resolution) {
            // Что-то делаем
        })
"""
