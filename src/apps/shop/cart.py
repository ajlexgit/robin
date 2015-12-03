import re
from django.views.generic import View
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
        self._counts = ()

    def __bool__(self):
        return bool(self._products)

    def __iter__(self):
        return iter(self._products)

    @property
    def products(self):
        return self._products

    @property
    def products_counts(self):
        return zip(self._products, self._counts)

    @property
    def products_prices_counts(self):
        return ((prod, prod.price * count, count) for prod, count in self.products_counts)

    @property
    def total_count(self):
        return sum(self._counts)

    @property
    def total_cost(self):
        return sum(prod.price * count for prod, count in self.products_counts)

    def _format(self):
        """
            Превращает неформатированный словарь self._unformatted вида {ID: count}
            в кортеж self._products вида с элементами (Product, count, price*count)
        """
        counts = []
        products = []
        for product in ShopProduct.objects.filter(id__in=self._unformatted):
            count = self._unformatted[product.id]
            if count > 0:
                count = max(0, count)
            if options.MAX_PRODUCT_COUNT:
                count = min(count, options.MAX_PRODUCT_COUNT)
            if count:
                counts.append(count)
                products.append(product)

        self._counts = tuple(counts)
        self._products = tuple(products)

    def clear(self, request, response=None):
        """
            Очистка корзины и данных сессии
        """
        self._unformatted = {}
        self._products = ()
        self._counts = ()

        try:
            del request.session[options.SESSION_CART_NAME]
        except KeyError:
            pass

        if response:
            response.set_cookie('clear_cart', '1', path='/')

    @classmethod
    def from_session(cls, request):
        """
            Заполнение объекта из сессии
        """
        cart = cls()

        cart._unformatted = {}
        data = request.session.get(options.SESSION_CART_NAME) or {}
        for product_id, count in data.items():
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
            Информация извлекается из полей вида "cart[ID]=count"
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

    @classmethod
    def from_order(cls, order):
        """
            Заполнение объекта из заказа
        """
        cart = cls()

        cart._unformatted = {}
        data = {order_item.product_id: order_item.count for order_item in order.order_products.all()}
        for product_id, count in data.items():
            try:
                product_id = int(product_id)
            except (TypeError, ValueError):
                continue

            cart._unformatted[product_id] = count

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
        cart = CartProducts.from_session(request)
        cart.clear(request)
        return self.json_response()
