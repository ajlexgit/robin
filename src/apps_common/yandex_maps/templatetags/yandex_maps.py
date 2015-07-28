from django.template import Library
from ..api import get_static_map_url, get_external_map_url, get_interactive_map_tag
from ..models import geocode_cached

register = Library()


@register.filter(is_safe=True)
def yandex_map_static(address, params=None):
    """
    Фильтр, который возвращает URL картинки с картой.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру YmapCoords

    Параметры:
        уровень детализации, ширина, высота - через запятую.

    Пример:

        <img src='{{ address|yandex_map_static:"15,300,200" }}'>
    """
    if not address:
        return ''

    if params is None:
        params = []
    else:
        params = [int(param.strip()) for param in params.split(",")]

    lng, lat = geocode_cached(address)
    return get_static_map_url(lng, lat, *params)


@register.filter(is_safe=True)
def yandex_map_external(address, zoom=14):
    """
    Фильтр, который возвращает URL карты у яндекса.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру YmapCoords

    Принимает 1 необязательный параметр: уровень детализации.

    Пример:

        <a href='{{ address|yandex_map_external:15 }}' target='_blank'>посмотреть карту</a>
    """
    if not address:
        return ''

    lng, lat = geocode_cached(address)
    return get_external_map_url(lng, lat, zoom)


@register.simple_tag
def yandex_map_interactive(address=None, **kwargs):
    """
    Тег, который выводит <div> с интерактивной картой.
    На странице должны быть подключены JS Яндекс Карт и скрипт инициализации

    Параметры:
        address: Координаты или адрес стартовой локации
        zoom: Начальный зум
        width: Ширина
        height: Высота

    Необходимо подключить JS:
        yandex_maps/js/yandex_maps.js

    Пример:
        {% yandex_map_interactive address=company.coords height=400 %}
        {% yandex_map_interactive address='Тольятти, Мира 6' zoom=14 %}
    """
    if address:
        lng, lat = geocode_cached(address)
        return get_interactive_map_tag(lng, lat, **kwargs)
    else:
        return get_interactive_map_tag(**kwargs)
