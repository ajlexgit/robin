import xml
from urllib import parse, request, error
from django.conf import settings
from django.forms.utils import flatatt

STATIC_MAPS_URL = 'http://static-maps.yandex.ru/1.x/?'
HOSTED_MAPS_URL = 'http://maps.yandex.ru/?'
GEOCODE_URL = 'http://geocode-maps.yandex.ru/1.x/?'

YANDEX_KEY = getattr(settings, 'YANDEX_MAPS_API_KEY', 'AES6VU8BAAAAhUgqJAIAFUXpiA6FBbStP2IMXobI37-poNIAAAAAAAAAAABFcoRJbRZ1Wym2ZqKgqBHebe4FPQ==')


def _format_point(longitude, latitude):
    return '%0.7f,%0.7f' % (float(longitude), float(latitude),)


def get_static_map_url(longitude, latitude, zoom=14, width=None, height=None):
    """ Возвращает URL статичной карты Яндекса """
    if not latitude or not longitude:
        return ''

    width = width or getattr(settings, 'YANDEX_MAPS_STATIC_WIDTH', 300)
    height = height or getattr(settings, 'YANDEX_MAPS_STATIC_HEIGHT', 200)
    point = _format_point(longitude, latitude)

    return STATIC_MAPS_URL + parse.urlencode(dict(
        ll=point,
        size='%d,%d' % (width, height,),
        z=zoom,
        l='map',
        pt=point,
        lang=settings.LANGUAGE_CODE,
        key=YANDEX_KEY,
    ))


def get_external_map_url(longitude, latitude, zoom=14):
    """ Возвращает URL карты на сервисе Яндекс.Карты """
    if not latitude or not longitude:
        return ''

    point = _format_point(longitude, latitude)

    return HOSTED_MAPS_URL + parse.urlencode(dict(
        ll=point,
        pt=point,
        l='map',
        z=zoom,
    ))


def get_interactive_map_tag(longitude, latitude,
                            zoom=14,
                            width=None, height=None,
                            header='', content='',
                            hidden=False):
    """ Возвращает тэг, который будет превращен JS-скриптом в интерактивную Яндекс-карту
    Параметры:
        zoom - начальное значение уровня детализации
        width - ширина карты
        height - высота карты
        header - заголовок балуна
        content - содержимое балуна
        hidden - должна ли карта быть по умолчанию скрыта
    """

    if not latitude or not longitude:
        return ''

    attrs = {
        'data-lng': longitude,
        'data-lat': latitude,
        'data-zoom': zoom,
        'data-header': header,
        'data-content': content,
    }

    styles = ''
    if width:
        styles += 'width: %spx;' % width
    if height:
        styles += 'height: %spx;' % height
    if hidden:
        styles += 'display: none;'
    attrs['style'] = styles

    return '<div class="yandex-map" %s></div>' % flatatt(attrs)


def geocode(address, timeout=5.0):
    """ Возвращает кортеж координат (longtitude, latitude,) по строке адреса """
    params = parse.urlencode({'geocode': address, 'key': YANDEX_KEY})
    try:
        response = request.urlopen(GEOCODE_URL + params, timeout=timeout)
    except error.URLError:
        return None

    try:
        dom = xml.dom.minidom.parseString(response.read())
        pos_elem = dom.getElementsByTagName('pos')[0]
        pos_data = pos_elem.childNodes[0].data
    except IndexError:
        return None

    return tuple(pos_data.split())
