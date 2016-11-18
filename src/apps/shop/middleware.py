from .cart import Cart

class CartMiddleware:
    """
        Добавляет в JSStorage флаг пустоты корзины.
        В списке MIDDLEWARE_CLASSES, должна быть ниже, чем JSStorageMiddleware.
    """
    @staticmethod
    def process_request(request):
        js_storage = getattr(request, 'js_storage', None)
        if js_storage is not None:
            cart = Cart.from_session(request)
            js_storage['session_cart_empty'] = not cart
