import inspect
from libs.cache import cached
from . import menus


@cached(time=10 * 60)
def get_menus():
    """ Получение всех меню, объявленных в файле menus.py """
    result = {}
    for name, func in inspect.getmembers(menus, inspect.isfunction):
        if func.__module__ == 'menu.menus':
            result[name] = func()

    return result


def activate_by_url(menu, url):
    """
        Активация пункта меню по урлу
    """
    if menu.is_active:
        return

    # пункты меню, которые соответсвуют урлу (префиксно)
    matches = [item for item in menu.items if url.startswith(item.url)]
    if not matches:
        return
    elif len(matches) == 1:
        matches[0].activate()
    else:
        # ищем самый длинный из совпавших урлов
        sorted_matches = sorted(matches, key=lambda item: len(item.url.split('/')), reverse=True)
        sorted_matches[0].activate()
