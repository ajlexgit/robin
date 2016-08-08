from .menus import *


class MenuMiddleware:
    @staticmethod
    def process_view(request, *args, **kwargs):
        """ Создание экземпляров меню """
        request._menus = {
            'main': get_main_menu(),
        }
        return

    @staticmethod
    def process_template_response(request, response):
        """
            Если в меню нет активного пункта, пытаемся его пределить по URL.
        """
        menus = getattr(request, '_menus', None)
        if not menus:
            return response

        if request.path_info == '/':
            return response

        for menu in menus.values():
            if menu.is_active:
                continue

            for item in menu.items:
                if request.path_info.startswith(item.url):
                    item.activate()
                    break

        return response
