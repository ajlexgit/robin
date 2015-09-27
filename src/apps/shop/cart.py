import re
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from libs.valute_field import Valute
from .models import ShopProduct
from . import options


class CartProducts:
    """
        Список товаров в корзине
    """
    def __init__(self):
        self._unformatted = {}
        self._products = ()

    def __bool__(self):
        return bool(self._products)

    def __iter__(self):
        return iter(self._products)

    @property
    def products(self):
        return self._products

    @property
    def total_cost(self):
        result = sum(item[2] for item in self._products)
        return Valute(result)

    def _format(self):
        """
            Превращает неформатированный словарь self._unformatted вида {SN: count}
            в кортеж self._products вида {Product, count, price*count}
        """
        products = ShopProduct.objects.filter(serial__in=self._unformatted)

        result = []
        for product in products:
            count = self._unformatted[product.serial]
            if count > 0:
                count = max(0, count)
            if options.MAX_PRODUCT_COUNT:
                count = min(count, options.MAX_PRODUCT_COUNT)
            if count:
                result.append((product, count, product.price * count))

        self._products = tuple(result)

    def clear(self, request):
        """
            Очистка корзины и данных сессии
        """
        self._unformatted = {}
        self._products = ()

        try:
            del request.session[options.SESSION_CART_NAME]
        except KeyError:
            pass

    @classmethod
    def from_session(cls, request):
        """
            Заполнение объекта из сессии
        """
        cart = cls()
        cart._unformatted = request.session.get(options.SESSION_CART_NAME, {})
        cart._format()
        return cart

    @classmethod
    def from_data(cls, data, fieldname='cart'):
        """
            Заполнение объекта из GET или POST-данных.
            Информация извлекается из полей вида "cart[SN]=count"
        """
        re_items_key = re.compile('^{}\[([-\w]+)\]$'.format(fieldname))

        cart = cls()
        cart._unformatted = {}
        for query_key, value in data.items():
            match = re_items_key.match(query_key)
            if not match:
                continue

            sn = match.group(1)
            try:
                value = int(value)
            except (TypeError, ValueError):
                value = 0

            cart._unformatted[sn] = value

        cart._format()
        return cart

    def to_session(self, request):
        """
            Сохранение данных в сессию
        """
        request.session[options.SESSION_CART_NAME] = self._unformatted


@require_POST
def save_cart(request):
    """ Установка всех товаров в корзине """
    cart = CartProducts.from_data(request.POST)
    cart.to_session(request)
    return JsonResponse({

    })