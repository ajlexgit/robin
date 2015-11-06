import re
from django.views.generic import View
from libs.valute_field import Valute
from libs.views_ajax import AjaxViewMixin
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
            Превращает неформатированный словарь self._unformatted вида {ID: count}
            в кортеж self._products вида {Product, count, price*count}
        """
        products = ShopProduct.objects.filter(id__in=self._unformatted)

        result = []
        for product in products:
            count = self._unformatted[product.id]
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

        cart._unformatted = {}
        data = request.session.get(options.SESSION_CART_NAME, {})
        for product_id, count in data:
            try:
                product_id = int(product_id)
            except (TypeError, ValueError):
                continue

            cart._unformatted[product_id] = count

        cart._format()
        return cart

    @classmethod
    def from_data(cls, data, fieldname='cart'):
        """
            Заполнение объекта из GET или POST-данных.
            Информация извлекается из полей вида "cart[SN]=count"
        """
        re_items_key = re.compile('^{}\[(\d+)\]$'.format(fieldname))

        cart = cls()
        cart._unformatted = {}
        for query_key, value in data.items():
            match = re_items_key.match(query_key)
            if not match:
                continue

            product_id = match.group(1)
            try:
                product_id = int(product_id)
            except (TypeError, ValueError):
                continue

            try:
                value = int(value)
            except (TypeError, ValueError):
                value = 0

            cart._unformatted[product_id] = value

        cart._format()
        return cart

    def to_session(self, request):
        """
            Сохранение данных в сессию
        """
        request.session[options.SESSION_CART_NAME] = self._unformatted



class SaveCart(AjaxViewMixin, View):
    def post(self, request):
        """ Установка всех товаров в корзине """
        cart = CartProducts.from_data(request.POST)
        cart.to_session(request)
        return self.json_response()


class ClearCart(AjaxViewMixin, View):
    def post(self, request):
        """ Очистка корзины """
        cart = CartProducts.from_data(request.POST)
        cart.to_session(request)
        return self.json_response()
