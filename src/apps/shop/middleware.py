from libs.cookies import set_cookie, delete_cookie
from .cart import Cart
from . import conf


class CartMiddleware:
    """
        Копирование корзины из сессии в куку, для доступа к ней через JS.
    """
    @staticmethod
    def process_response(request, response):
        js_storage = getattr(request, 'js_storage', None)
        if js_storage is not None:
            js_storage['shop_cart_cookie'] = conf.COOKIE_CART_NAME

            cart = Cart.from_session(request)
            cart_cookie = request.COOKIES.get(conf.COOKIE_CART_NAME)
            cart_value = ':'.join(map(str, [cart.total_count, cart.total_price.as_string()]))
            if cart and cart_cookie != cart_value:
                set_cookie(response, conf.COOKIE_CART_NAME, cart_value)
            elif not cart and cart_cookie is not None:
                delete_cookie(response, conf.COOKIE_CART_NAME)

        return response
