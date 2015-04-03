from .menu import Menu

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
            url='posts:detail',
            url_args=(),
            url_kwargs={
                'post_id': 2,
            },

            # Жестко указанная ссылка
            url='http://ya.ru/',

            # Аттрибуты ссылки
            attrs={
                'target': '_blank',
            },

            # CSS-классы пункта меню
            classes=('red', ),

            # Дочерние пункты меню
            childs=[],
        )


    Также можно создавать меню на лету, пользуясь методами списка меню:
        menu = Menu(request)
        menu.root.add(
            MenuItem('Test', '/test/').childs.add(
                MenuItem('Subtest1', '/subtest/'),
            ),
            MenuItem('Test2', '/test2/'),
        )
        menu.root.insert(
            MenuItem('Test3', '/test3/'),
        )
        menu.render(template='menu/menu.html')
"""