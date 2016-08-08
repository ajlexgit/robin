"""
    Меню сайта.

    Установка:
        INSTALLED_APPS = (
            ...
            'menu',
            ...
        )

        MIDDLEWARE_CLASSES = (
            ...
            'menu.middleware.MenuMiddleware',
            ...
        )

    Пример:
        # menu/menus.py
            menu = Menu()
            menu.append(
                MenuItem('News', '/news/').append(
                    MenuItem('Post 1', '/news/post-1/'),
                    MenuItem('Post 2', '/news/post-2/'),
                ),
                MenuItem('Articles', '/articles/', search_id='articles'),
            )

        # template.html
            {% load menu %}

            ...
            {% menu 'main' %}
            ...

        # views.py:
            from menu import activate_menu
            ...
            # Ручная установка активного пункта меню по его search_id
            activate_menu(request, search_id='articles')
"""

def activate_menu(request, search_id):
    """
        Активация пункта во всех меню по его search_id.
    """
    menus = getattr(request, '_menus', None)
    if not menus:
        return

    for menu in menus.values():
        if menu.is_active:
            continue

        for item in menu.items:
            if item.search_id == search_id:
                item.activate()
                break
