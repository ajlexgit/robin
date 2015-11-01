"""
    Зависит от:
        libs.coords

    Необходимо подключить:
        yandex_maps/js/core.js

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'yandex_maps',
                ...
            )

    Настройки (settings.py):
        YANDEX_MAPS_API_KEY - ключ
        ADMIN_YANDEX_MAP_WIDTH - ширина карты в админке (по умолчанию 100%)
        ADMIN_YANDEX_MAP_HEIGHT - высота карты в админке (по умолчанию 300px)

        YANDEX_MAPS_STATIC_WIDTH - ширина статических карт по умолчанию
        YANDEX_MAPS_STATIC_HEIGHT - высота статических карт по умолчанию

    Примеры:
        script.py:
            from yandex_maps import *

            # Получить координаты по адресу.
            lng, lat = geocode('Тольятти, Мира 35', timeout=0.5)

            # Получить координаты по адресу с кэшированием результатов
            lng, lat = geocode_cached('Тольятти, Мира 35', timeout=0.5)

        models.py:
            from yandex_maps import YandexCoordsField
            ...

            address = models.CharField(_('address'), max_length=255, blank=True)
            coords = YandexCoordsField(_('coordinates'), null=True, blank=True)

        page.js:
            $(document).on('google-maps-ready', function() {
                var ymap = YandexMap.create('#ymap');
                ymap.addPlacemark({
                    lng: 49.418785,
                    lat: 53.510171,
                    hint: 'First',
                    balloon: '<p>Hello</p>'
                });
            });

        Admin Javascript:
            // Получение координат по адресу в другом поле
            $(document).on('change', '#id_address', function() {
                var ymap = $('#id_coords').next('.yandex-map').data('map');
                ymap.geocode($(this).val(), function(point) {
                    var placemark = this.getPlacemark();
                    if (placemark) {
                        placemark.moveTo(point);
                    } else {
                        placemark = this.addPlacemark({
                            point: point
                        });
                    }

                    this.panTo(placemark.point);
                });
            });

        template.html:
            {% load yandex_maps %}

            <!-- Статичная карта с зумом 15 размера 300x200 -->
            <img src='{{ address|yandex_map_static:"15,300,200" }}'>

            <!-- Ссылка на карту в сервисе Яндекса -->
            <a href='{{ address|yandex_map_external:15 }}' target='_blank'>посмотреть карту</a>
"""

from .api import geocode
from .models import geocode_cached
from .fields import YandexCoordsField
from .widgets import YandexCoordsAdminWidget

__all__ = ['geocode', 'geocode_cached', 'YandexCoordsField']