import inspect
from . import menus


def get_menus(request):
    """ Получение всех меню, объявленных в файле menus.py """
    result = {}
    for name, func in inspect.getmembers(menus, inspect.isfunction):
        if func.__module__ == 'menu.menus':
            result[name] = func(request)

    return result


class MenuMiddleware:
    @staticmethod
    def process_request(request):
        """ Создание экземпляров меню """
        request._menus = get_menus(request)
        return

    @staticmethod
    def process_template_response(request, response):
        """
            Если в меню нет активного пункта, пытаемся его определить по URL.
        """
        menus = getattr(request, '_menus', None)
        if not menus:
            return response

        if request.path_info == '/':
            return response

        current_url = request.path_info
        for menu in menus.values():
            if menu.is_active:
                continue

            for item in menu.items:
                if current_url.startswith(item.url):
                    item.activate()
                    break

        return response
