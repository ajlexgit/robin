import math
import requests
from hashlib import md5
from django.core.cache import caches
from libs.associative_request import associative


METHOD_KEYS = {
    'getPaymentMethods': 'b925c7c8dbc471e0a7724670804db66fb2f3752ed0b8f5dab9442c554c896f93',
    'getSenderOrders': 'b925c7c8dbc471e0a7724670804db66f364683c8e19e234954f89a7a071ea062',
    'getSenderOrderLabel': 'b925c7c8dbc471e0a7724670804db66f874378746de0bf7c34dc179b6dc6efbf',
    'getSenderParcelDocs': 'b925c7c8dbc471e0a7724670804db66f1245c98e77b8d06bbbaac0a7d309c850',
    'autocomplete': 'b925c7c8dbc471e0a7724670804db66f03302c240e70ba09d5c9c99e56b55161',
    'getIndex': 'b925c7c8dbc471e0a7724670804db66f72ba31964b0bd8f086c393febcfc24bc',
    'createOrder': 'b925c7c8dbc471e0a7724670804db66f75a8635b7ae3ea8b572703c234d250f6',
    'updateOrder': 'b925c7c8dbc471e0a7724670804db66fa94ced5545187cea0db6dee1f4badab2',
    'deleteOrder': 'b925c7c8dbc471e0a7724670804db66f2181dbc11e5914fd1f03528ad89fbd4c',
    'getSenderOrderStatus': 'b925c7c8dbc471e0a7724670804db66f96194c01b595bbbd4b3bf377b2eefaf6',
    'getSenderOrderStatuses': 'b925c7c8dbc471e0a7724670804db66f6b7a1f50371e87589d511e0ae5a49cd1',
    'getSenderInfo': 'b925c7c8dbc471e0a7724670804db66ff0b8ed707c2855da544d733f6185b55d',
    'getWarehouseInfo': 'b925c7c8dbc471e0a7724670804db66f43fbdac73766be5867828b8164309432',
    'getRequisiteInfo': 'b925c7c8dbc471e0a7724670804db66f57a55d0d67b328e287568d68cb3de8d8',
    'getIntervals': 'b925c7c8dbc471e0a7724670804db66ffebb7f623f4ea9c13a09ac6d6b84a184',
    'createWithdraw': 'b925c7c8dbc471e0a7724670804db66f588ab118bbcffc1f430f6597f2bc08f5',
    'confirmSenderOrders': 'b925c7c8dbc471e0a7724670804db66ffdd35c30eaef11fb7cd8621ed78d9989',
    'updateWithdraw': 'b925c7c8dbc471e0a7724670804db66fb522b3d7426d0e98981dcb3b2ac69d51',
    'createImport': 'b925c7c8dbc471e0a7724670804db66febae75aa7596d897aef947881c479273',
    'updateImport': 'b925c7c8dbc471e0a7724670804db66f82cd71d6513599b318ab9f8edac17d9c',
    'getDeliveries': 'b925c7c8dbc471e0a7724670804db66f76d46bbfed869e4ae4b3a830819a3c55',
    'getOrderInfo': 'b925c7c8dbc471e0a7724670804db66f507bd772d21a1d14827a7a0c40f37ca2',
    'searchDeliveryList': 'b925c7c8dbc471e0a7724670804db66f738908a96eaff91b7e64958800ffb6c2',
    'confirmSenderParcels': 'b925c7c8dbc471e0a7724670804db66f6d6482b79564bede70b04bb692fa59e9'
}
CLIENT_ID = 1468
SENDER_ID = 664
WAREHOUSE_ID = 454
REQUISITE_ID = 418
API_URL = 'https://delivery.yandex.ru/api/1.0/'

CACHE = caches['default']
CACHE_TIME = 3 * 3600
AUTOCOMPLETE_CITY = 'locality'
AUTOCOMPLETE_STREET = 'street'
AUTOCOMPLETE_HOUSE = 'house'
AUTOCOMPLETE_TYPES = (AUTOCOMPLETE_CITY, AUTOCOMPLETE_STREET, AUTOCOMPLETE_HOUSE)


def _cache_key(*args):
    values = [CLIENT_ID, SENDER_ID]
    values.extend(args)
    return ':'.join(str(item) for item in values)


def _format_value(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, bytes):
        return value.decode()
    elif isinstance(value, list):
        return ''.join(_format_value(item) for item in value)
    elif isinstance(value, dict):
        sorted_keys = sorted(value.keys())
        return ''.join(_format_value(value[key]) for key in sorted_keys)
    else:
        return str(value)


def _make_secret(method, data):
    """ Получение секретного ключа для запроса """
    hasher = md5()
    hasher.update(_format_value(data).encode() + METHOD_KEYS.get(method).encode())
    return hasher.hexdigest()


def _request(method, data):
    data['secret_key'] = _make_secret(method, data)
    url = '%s%s' % (API_URL, method)
    response = requests.post(url, data=associative(data))
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError('API response: %s' % response.status_code)


def getPaymentMethods():
    """ Получение возможных способов оплаты заказа получателем. """
    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
    }
    return _request('getPaymentMethods', data)


def getSenderInfo():
    """ Получение информации о магазине из аккаунта в сервисе. """
    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
    }

    return _request('getSenderInfo', data)


def getWarehouseInfo():
    """ Получение данных о складе из аккаунта в сервисе. """
    cache_key = _cache_key(WAREHOUSE_ID)
    if cache_key in CACHE:
        return CACHE.get(cache_key)

    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
        'warehouse_id': WAREHOUSE_ID,
    }

    result = _request('getWarehouseInfo', data)
    CACHE.set(cache_key, result, CACHE_TIME)
    return result


def getRequisiteInfo():
    """ Получение информации о реквизитах магазина из аккаунта в сервисе. """
    cache_key = _cache_key(REQUISITE_ID)
    if cache_key in CACHE:
        return CACHE.get(cache_key)

    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
        'requisite_id': REQUISITE_ID,
    }

    result = _request('getRequisiteInfo', data)
    CACHE.set(cache_key, result, CACHE_TIME)
    return result


def searchDeliveryList(city_from, city_to, weight, height, width, length, **kwargs):
    """ Получение доступных вариантов доставки """
    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
        'city_from': str(city_from),
        'city_to': str(city_to),
        'weight': float(weight),
        'height': int(height),
        'width': int(width),
        'length': int(length),
    }

    nonrequired = ('delivery_type', 'total_cost', 'index_city', 'create_date', 'payment_method')
    for name in nonrequired:
        value = kwargs.get(name)
        if value:
            data[name] = value

    return _request('searchDeliveryList', data)


def promoDeliveryList(city_to, default_weight=None, default_width=None, default_height=None, default_length=None,
        **kwargs):
    """ Получение доступных вариантов доставки для среднего заказа """
    warehouse = getWarehouseInfo()

    # определяем умолчания
    if not any((default_weight, default_width, default_height, default_length)):
        requisite = getRequisiteInfo()
        promo = requisite['data']['promoRequest']
        default_weight = default_weight or promo['weight']
        default_width = default_width or promo['width']
        default_height = default_height or promo['height']
        default_length = default_length or promo['length']

    city_from = warehouse['data']['address_model']['city']
    weight = kwargs.pop('weight', default_weight)
    width = kwargs.pop('width', default_width)
    height = kwargs.pop('height', default_height)
    length = kwargs.pop('length', default_length)

    return searchDeliveryList(city_from, city_to, weight, height, width, length, **kwargs)


def autocomplete(term, object_type=AUTOCOMPLETE_CITY, city=None, street=None):
    """ Автоматическое дополнение названий города, улицы и дома. """
    if object_type not in AUTOCOMPLETE_TYPES:
        raise ValueError('undefined autocomplete type: %s' % object_type)

    if object_type != AUTOCOMPLETE_CITY and not city:
        raise ValueError('city required for this type')

    if object_type == AUTOCOMPLETE_HOUSE and not street:
        raise ValueError('street required for this type')

    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
        'term': str(term),
        'type': object_type
    }

    if city:
        data['locality_name'] = str(city)

    if street:
        data['street'] = str(street)

    return _request('autocomplete', data)


def getIndex(address):
    """ Определение индекса по указанному адресу. """
    cache_key = _cache_key(address)
    if cache_key in CACHE:
        return CACHE.get(cache_key)

    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
        'address': str(address),
    }

    result = _request('getIndex', data)
    CACHE.set(cache_key, result, CACHE_TIME)
    return result


def getDeliveries():
    """ Получение наименований доступных служб доставки и сортировочных центров. """
    cache_key = _cache_key()
    if cache_key in CACHE:
        return CACHE.get(cache_key)

    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
    }

    result = _request('getDeliveries', data)
    CACHE.set(cache_key, result, CACHE_TIME)
    return result


def createOrder(
        first_name='', last_name='', phone='', email='', comment='',
        order_weight=1, order_length=None, order_width=None, order_height=None,
        order_num=None, payment_method=None, products_cost=None, delivery_cost=None,
        city=None, street=None, house=None,
        delivery_id=None, order_items=()
    ):
    """
        Создание заказа со статусом черновика.

        order_items:
        {
            'orderitem_article': 'AB1',
            'orderitem_name': 'Товар',
            'orderitem_quantity': '3',
            'orderitem_cost': '1'
        }
    """
    data = {
        'client_id': CLIENT_ID,
        'sender_id': SENDER_ID,
    }

    if first_name:
        data['recipient_first_name'] = str(first_name)
    if last_name:
        data['recipient_last_name'] = str(last_name)
    if phone:
        data['recipient_phone'] = str(phone)
    if email:
        data['recipient_email'] = str(email)
    if comment:
        data['recipient_comment'] = str(comment)

    # определяем умолчания
    if not all((order_weight, order_width, order_height, order_length)):
        requisite = getRequisiteInfo()
        promo = requisite['data']['promoRequest']
        order_weight = order_weight or promo['weight']
        order_width = order_width or promo['width']
        order_height = order_height or promo['height']
        order_length = order_length or promo['length']

    data['order_weight'] = str(math.ceil(order_weight))
    data['order_width'] = str(order_width)
    data['order_height'] = str(order_height)
    data['order_length'] = str(order_length)

    if order_num:
        data['order_num'] = int(order_num)

    data['order_requisite'] = REQUISITE_ID
    data['order_warehouse'] = WAREHOUSE_ID

    if payment_method:
        data['order_payment_method'] = int(payment_method)
    if products_cost:
        data['order_assessed_value'] = int(products_cost)
    if delivery_cost:
        data['order_delivery_cost'] = int(delivery_cost)

    if city:
        data['deliverypoint_city'] = str(city)
    if street:
        data['deliverypoint_street'] = str(street)
    if house:
        data['deliverypoint_house'] = str(house)

    if delivery_id:
        data['delivery_delivery'] = int(delivery_id)

    if order_items:
        for item in order_items:
            item['orderitem_cost'] = math.ceil(item['orderitem_cost'])
        data['order_items'] = order_items

    return _request('createOrder', data)
