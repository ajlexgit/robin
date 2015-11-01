import xml
from urllib import parse, request, error
from django.conf import settings

STATIC_MAPS_URL = 'http://maps.googleapis.com/maps/api/staticmap?'
HOSTED_MAPS_URL = 'http://maps.google.com/maps?'
GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/xml?'

# Координаты, возвращаемые в случае, если настоящие координаты не определены
DEFAULT = (49.418785, 53.510171)


def _format_point(longitude, latitude):
    return '%0.7f,%0.7f' % (float(latitude), float(longitude),)


def get_static_map_url(longitude, latitude, zoom=14, width=None, height=None):
    """ Возвращает URL статичной карты Google """
    if not latitude or not longitude:
        longitude, latitude = DEFAULT

    width = width or getattr(settings, 'GOOGLE_MAPS_STATIC_WIDTH', 300)
    height = height or getattr(settings, 'GOOGLE_MAPS_STATIC_HEIGHT', 200)
    point = _format_point(longitude, latitude)

    return STATIC_MAPS_URL + parse.urlencode(dict(
        center=point,
        size='%dx%d' % (width, height,),
        zoom=zoom,
        maptype='roadmap',
        language=settings.SHORT_LANGUAGE_CODE,
        markers='color:red|label:G|%s' % point,
    ))


def get_external_map_url(longitude, latitude, zoom=14):
    """ Возвращает URL карты на сервисе Google """
    if not latitude or not longitude:
        longitude, latitude = DEFAULT

    point = _format_point(longitude, latitude)

    return HOSTED_MAPS_URL + parse.urlencode(dict(
        q='loc:%s' % point,
        t='r',
        hl=settings.SHORT_LANGUAGE_CODE,
        z=zoom,
    ))


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
