"""
    Меню сайта.

    Установка:
        INSTALLED_APPS = (
            ...
            'menu',
            ...
        )

    Можно создать объект меню, передав ему список пунктов меню из конфигурации:
        menu = Menu(request, config_list)

    Формат пункта меню:
        dict(
            # Текст ссылки
            title='Публикация 2',

            # Ссылка, геренируемая по шаблону
            url='module:detail',
            url_args=(),
            url_kwargs={
                'post_id': 2,
            },

            # Аттрибуты ссылки
            attrs={
                'target': '_blank',
            },

            # Дочерние пункты меню
            childs=[],
        )


    Также можно создавать меню на лету, пользуясь методами списка меню:
        menu = Menu(request)
        menu.append(
            MenuItem('Test', '/test/').append(
                MenuItem('Subtest1', '/subtest/'),
            ),
            MenuItem('Test2', '/test2/'),
        )
        menu.insert(0,
            MenuItem('Test3', '/test3/'),
        )
        menu.render(template='menu/menu.html')
"""

from .menu import Menu