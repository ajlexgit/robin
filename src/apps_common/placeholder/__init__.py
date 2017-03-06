"""
    Модуль, расставляющий заглушки для блоков, которые будут подгружены через AJAX.

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'placeholder',
                ...
            )

            PIPELINE = {
                ...
                'placeholder/js/placeholder.js',
                ...
            }

        urls.py:
            ...
            url(r'^placeholder/', include('placeholder.urls', namespace='placeholder')),
            ...

    1) Помимо имени в {% placeholder %} можно указывать любое кол-во дополнительных
       параметров, которые должны быть сериализуемы, т.к. они превращаются в data-атрибуты
       тэга заглушки
    2) Заглушка с одним именем может встречаться на странице несколько раз с разными параметрами.
       Каждое такое появление называется "часть заглушки".
    3) На каждое имя регистрируется функция-обработчик, которая должна вернуть
       одну или несколько отрендеренных частей в виде итератора
    4) Функция должна быть зарегистрирована в apps.py

    Пример:
        # apps.py:
            def ready(self):
                from placeholder import register_placeholder
                from .views_ajax import contact_block_placeholder
                register_placeholder('contact_block', contact_block_placeholder)

        # views.py:
            def contact_block_placeholder(request, name, parts):
                return [
                    build_block_part(request, name, **part_params)
                    for part_params in parts
                ]

            def build_block_part(request, name, **params):
                bg = params.get('bg', 'yellow)
                if not bg:
                    return ''

                title = params.get('bg', 'Join us')
                return loader.render_to_string('contact_block/part.html', {
                    'bg': bg,
                    'title': title,
                }, request=request)


        # template.html:
            {% load placeholder %}

            {% placeholder "contact_block" bg="red" %}
            {% placeholder "contact_block" bg="blue" title="Hello" %}

"""
from .utils import register_placeholder

default_app_config = 'placeholder.apps.Config'
