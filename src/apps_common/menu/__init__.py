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
            def main():
                menu = Menu()
                menu.append(
                    MenuItem('News', '/news/').append(
                        MenuItem('Post 1', '/news/post-1/'),
                        MenuItem('Post 2', '/news/post-2/'),
                    ),
                    MenuItem('Articles', '/articles/', item_id='articles'),
                )
                return menu

        # template.html
            ...
            {% menu 'main' %}
            ...

        # views.py:
            from menu import activate_menu
            ...
            # Ручная установка активного пункта меню по его item_id
            activate_menu(request, 'articles')
"""

def activate_menu(request, item_id):
    """
        Активация пункта во всех меню по его item_id.
    """
    menus = getattr(request, '_menus', None)
    if not menus:
        return

    for menu in menus.values():
        if menu.is_active:
            continue

        for item in menu.items:
            if item.item_id == item_id:
                item.activate()
                break
