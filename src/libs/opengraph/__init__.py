OPENGRAPH = {}

"""
    Тэги Opengraph.
    
    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'libs.opengraph',
                ...
            )
            
            MIDDLEWARE_CLASSES = (
                ...
                'libs.opengraph.middleware.OpengraphMiddleware',
                ...
            )
    
    Пример использования:
        views.py:
            def my_page(request):
                ...
                request.opengraph.update({
                    'fb:app_id': '229798780479496',
                    'url': request.build_absolute_uri(),
                    'title': post.title,
                    'image': request.build_absolute_uri(post.preview.url),
                    'description': description(strip_tags(post.text), 50, 150),
                })
                ...
    
        # Можно объявлять переменные для всего сайта:
        apps.py:
            class Config(AppConfig):
                name = 'users'
                verbose_name = "Пользователи"
                
                def ready(self):
                    from libs.opengraph import OPENGRAPH
                    OPENGRAPH.update({
                        'fk:app': '12345'
                    })
    
        template.html:
            {% load opengraph %}
            ...
            {% opengraph %}

"""