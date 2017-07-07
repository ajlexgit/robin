import requests
from libs.associative_request import associative
from . import conf


def request(api_method, method=None, params=None, data=None):
    """ Запрос к API """
    params = params or {}
    params = dict({
        'token': conf.API_TOKEN,
        'method': api_method,
    }, **params)

    method = method or 'GET' if not data else 'POST'
    response = requests.request(method, conf.API_URL,
        params=associative(params),
        data=associative(data),
        timeout=(5, 10),
    )

    try:
        data = response.json()
    except ValueError:
        return None

    # if 'error' in data:
    #     raise SubscribeAPIError(data['error']['code'], data['error']['message'])

    return data


def getCities():
    """
        Позволяет получить список городов, в которых есть пункты выдачи.

        Поля ответа:
            'Name'                      => 'Наименование города',
            'Code'                      => 'Код города в boxberry',
            'Prefix'                    => 'Префикс: г - Город, п - Поселок и т.д',
            'ReceptionLaP'              => 'Прием пип',
            'DeliveryLaP'               => 'Выдача пип',
            'Reception'                 => 'Прием МиМ',
            'ForeignReceptionReturns'   => 'Прием международных возвратов',
            'Terminal'                  => 'Наличие терминала',
            'Kladr'                     => 'ИД КЛАДРа',
            'Region'                    => 'Регион',
            'CountryCode'               => 'Код страны',
            'UniqName'                  => 'Составное уникальное имя',
            'District'                  => 'Район'
    """
    return request('ListCities')


def getCitiesCourier():
    """
        Позволяет получить список городов в которых осуществляется курьерская доставка.

        Поля ответа:
            'City'              => 'Населенный пункт',
            'Region'            => 'Регион',
            'Area'              => 'Область',
            'DeliveryPeriod'    => 'Срок доставки',
    """
    return request('CourierListCities')


def getCitiesFull():
    """
        Позволяет получить список городов, в которых осуществляется доставка Boxberry.

        Поля ответа:
            'Name'                      => 'Наименование города',
            'Code'                      => 'Код города в boxberry',
            'Prefix'                    => 'Префикс: г - Город, п - Поселок и т.д',
            'ReceptionLaP'              => 'Прием пип',
            'DeliveryLaP'               => 'Выдача пип',
            'Reception'                 => 'Прием МиМ',
            'ForeignReceptionReturns'   => 'Прием международных возвратов',
            'Terminal'                  => 'Наличие терминала',
            'Kladr'                     => 'ИД КЛАДРа',
            'Region'                    => 'Регион',
            'CountryCode'               => 'Код страны',
            'UniqName'                  => 'Составное уникальное имя',
            'District'                  => 'Район'
    """
    return request('ListCitiesFull')


def getPoints(city=None, prepaid=0):
    """
        Позволяет получить информацию о всех точках выдачи заказов.

        Параметры:
            city    - код города (в системе Boxberry, а не российский)
            prepaid - показать ПВЗ, работающие по предоплате

        По умолчанию возвращается список точек с возможностью оплаты при получении заказа.
        Если вам необходимо увидеть точки, работающие с предоплатой, передайте параметр "prepaid" равный 1.

        Поля ответа:
            'Code'              => 'Код в базе boxberry',
            'Name'              => 'Наименование ПВЗ',
            'Address'           => 'Полный адрес',
            'Phone'             => 'Телефон или телефоны',
            'WorkSchedule'      => 'График работы',
            'TripDescription'   => 'Описание проезда',
            'DeliveryPeriod'    => 'Срок доставки',
            'CityCode'          => 'Код города в boxberry',
            'CityName'          => 'Наименование города',
            'TariffZone'        => 'Тарифная зона',
            'Settlement'        => 'Населенный пункт',
            'Area'              => 'Регион',
            'Country'           => 'Страна',
            'GPS'               => 'Координаты gps',
            'OnlyPrepaidOrders' => 'Точка работает только с полностью оплаченными заказами',
            'Acquiring'         => 'Есть возможность оплаты банковскими картами',
            'DigitalSignature'  => 'Подпись получателя будет хранится в системе boxberry в электронном виде'
    """
    return request('ListPoints', params={
        'CityCode': city,
        'prepaid': prepaid,
    })


def getDeliveryCosts(target, weight=500, orderprice=0, height=0, width=0, depth=0):
    """
        Позволяет узнать стоимость доставки посылки до ПВЗ.

        Параметры:
            target      - код ПВЗ
            weight      - вес посылки в граммах
            orderprice  - cтоимость товаров без учета стоимости доставки
            height      - высота коробки (см)
            width       - ширина коробки (см)
            depth       - глубина коробки (см)

        Поля ответа:
            'price'             => 'Итоговая цена в рублях',
            'price_base'        => 'Базовая стоимость',
            'price_service'     => 'Стоимость услуг',
            'delivery_period'   => 'Cрок доставки',
    """
    return request('DeliveryCosts', params={
        'target': target,
        'weight': weight,
        'ordersum': orderprice,
        'height': height,
        'width': width,
        'depth': depth,
    })


def getPoint(target, photos=False):
    """
        Позволяет получить всю информацию по ПВЗ, включая фотографии.

        Параметры:
            target      - код ПВЗ
            photos      - включить картинки в ответ

        Поля ответа (часть из них):
            'Name'              => 'Наименование ПВЗ',
            'Organization'      => 'Организация',
            'ZipCode'           => 'Индекс',
            'Address'           => 'Полный адрес',
            'AddressReduce'     => 'Короткий адрес',
            'Street'            => 'Улица',
            'House'             => 'Номер дома',
            'PrepaidOrdersOnly' => 'Выдача только предоплаченных заказов',
            'CourierDelivery'   => 'Осуществляет курьерскую доставку',
            'LoadLimit'         => 'Ограничение веса, кг',
            'VolumeLimit'       => 'Ограничение объема',
            'Photos'            => 'Массив с фотографиями в base64',
    """
    return request('PointsDescription', params={
        'code': target,
        'photo': int(photos),
    })
