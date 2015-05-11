import xml
from urllib import parse, request, error
from django.conf import settings
from django.forms.utils import flatatt

STATIC_MAPS_URL = 'http://maps.googleapis.com/maps/api/staticmap?'
HOSTED_MAPS_URL = 'http://maps.google.com/maps?'
GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/xml?'


def _format_point(latitude, longitude):
    return '%0.7f,%0.7f' % (float(latitude), float(longitude),)


def get_static_map_url(longitude, latitude, zoom=14, width=None, height=None):
    """ Возвращает URL статичной карты Google """
    if not latitude or not longitude:
        return ''

    width = width or getattr(settings, 'GOOGLE_MAPS_STATIC_WIDTH', 300)
    height = height or getattr(settings, 'GOOGLE_MAPS_STATIC_HEIGHT', 200)
    point = _format_point(latitude, longitude)

    return STATIC_MAPS_URL + parse.urlencode(dict(
        center=point,
        size='%dx%d' % (width, height,),
        zoom=zoom,
        maptype='roadmap',
        language=settings.LANGUAGE_CODE,
        markers='color:red|label:G|%s' % point,
    ))


def get_external_map_url(longitude, latitude, zoom=14):
    """ Возвращает URL карты на сервисе Google """
    if not latitude or not longitude:
        return ''

    point = _format_point(latitude, longitude)

    return HOSTED_MAPS_URL + parse.urlencode(dict(
        q='loc:%s' % point,
        t='r',
        hl=settings.LANGUAGE_CODE,
        z=zoom,
    ))


def get_interactive_map_tag(longitude, latitude,
                            zoom=14,
                            width=None, height=None,
                            header='', content='',
                            hidden=False):
    """
    Возвращает тэг, который будет превращен JS-скриптом в интерактивную Google-карту
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

    return '<div class="google-map" %s></div>' % flatatt(attrs)


def geocode(address, timeout=5.0):
    """ Возвращает кортеж координат (longtitude, latitude,) по строке адреса """
    params = parse.urlencode({'sensor': False, 'address': address})
    try:
        response = request.urlopen(GEOCODE_URL + params, timeout=timeout)
    except error.URLError:
        return None

    try:
        dom = xml.dom.minidom.parseString(response.read())
        location_elem = dom.getElementsByTagName('location')[0]
        lng = location_elem.getElementsByTagName('lng')[0]
        lat = location_elem.getElementsByTagName('lat')[0]
    except IndexError:
        return None

    return lng.firstChild.data, lat.firstChild.data
