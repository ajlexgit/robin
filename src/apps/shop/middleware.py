from .cart import Cart
from libs.cookies import set_cookie, delete_cookie

CART_COOKIE_NAME = 'cart-price'


class CartMiddleware:
    """
        Добавляет в куку корзины для того, чтобы кэширование страниц работало корректно.
        В списке MIDDLEWARE_CLASSES, должна быть выше, чем JSStorageMiddleware.
    """
    @staticmethod
    def process_response(request, response):
        js_storage = getattr(request, 'js_storage', None)
        if js_storage is not None:
            cart = Cart.from_session(request)
            cart_cookie = request.COOKIES.get(CART_COOKIE_NAME)
            cart_value = ':'.join(map(str, [cart.total_count, cart.total_price.as_string()]))
            if cart and cart_cookie != cart_value:
                set_cookie(response, CART_COOKIE_NAME, cart_value)
            elif not cart and cart_cookie is not None:
                delete_cookie(response, CART_COOKIE_NAME)

        return response
