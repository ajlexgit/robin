from django.template import Library
from ..api import get_static_map_url, get_external_map_url, get_interactive_map_tag
from ..models import geocode_cached

register = Library()


@register.filter
def static_map_url(address, params=None):
    """
    Фильтр, который возвращает URL картинки с картой.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру YmapCoord

    Параметры:
        уровень детализации, ширина, высота - через запятую.

    Пример:

        <img src='{{ address|static_map_url:"15,300,200" }}'>
    """
    if not address:
        return ''

    if params is None:
        params = []
    else:
        params = [int(param.strip()) for param in params.split(",")]

    lng, lat = geocode_cached(address)
    return get_static_map_url(lng, lat, *params)


@register.filter
def external_map_url(address, zoom=14):
    """
    Фильтр, который возвращает URL карты у яндекса.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру YmapCoord

    Принимает 1 необязательный параметр: уровень детализации.

    Пример:

        <a href='{{ address|external_map_url:15 }}' target='_blank'>посмотреть карту</a>
    """
    if not address:
        return ''

    lng, lat = geocode_cached(address)
    return get_external_map_url(lng, lat, zoom)


@register.simple_tag
def interactive_map(address=None, *args,  **kwargs):
    """
    Тег, который выводит <div> с интерактивной картой.
    На странице должны быть подключены JS Яндекс Карт и скрипт инициализации

    Параметры:
        address: Координаты или адрес стартовой локации
        zoom: Начальный зум
        width: Ширина
        height: Высота

    Необходимо подключить JS:
        //api-maps.yandex.ru/2.0/?load=package.full&lang=ru-RU
        yandex_maps/js/init.js

    Пример:
        {% interactive_map address=company.coords height=400 %}
        {% interactive_map address='Тольятти, Мира 6' zoom=14 %}
    """
    if not address:
        return ''

    lng, lat = geocode_cached(address)
    return get_interactive_map_tag(lng, lat, *args,  **kwargs)
