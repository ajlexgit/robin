"""
    Зависит от:
        libs.coords

    Необходимо подключить:
        google_maps/js/core.js

    Установка:
        settings.py:
            INSTALLED_APPS = (
                ...
                'google_maps',
                ...
            )

    Настройки (settings.py):
        ADMIN_GOOGLE_MAP_WIDTH - ширина карты в админке (по умолчанию 100%)
        ADMIN_GOOGLE_MAP_HEIGHT - высота карты в админке (по умолчанию 300px)

        GOOGLE_MAPS_STATIC_WIDTH - ширина статических карт по умолчанию
        GOOGLE_MAPS_STATIC_HEIGHT - высота статических карт по умолчанию

    Примеры:
        script.py:
            from google_maps import *

            # Получить координаты по адресу.
            lng, lat = geocode('Тольятти, Мира 35', timeout=0.5)

            # Получить координаты по адресу с кэшированием результатов
            lng, lat = geocode_cached('Тольятти, Мира 35', timeout=0.5)

        models.py:
            from google_maps import GoogleCoordsField
            ...

            address = models.CharField(_('address'), max_length=255, blank=True)
            coords = GoogleCoordsField(_('coordinates'), null=True, blank=True)

        page.js:
            $(document).ready(function() {
                var gmap = GoogleMap.create('#gmap');
                GoogleMap.ready(function() {
                    var point = gmap.createPoint(49.418785, 53.510171);
                    var marker = gmap.createMarker(point);
                    var bubble = gmap.createBubble('<p>Hello</p>');
                    gmap.addListener(marker, 'click', function() {
                        bubble.open(this.map, marker);
                    });
                });
            });

        Admin Javascript:
            // Получение координат по адресу в другом поле
            $(document).on('change', '#id_address', function() {
                var gmap = $('#id_coords').next('.google-map').data('map');
                gmap.geocode($(this).val(), function(point) {
                    if (this.marker) {
                        this.marker.setPosition(point);
                    } else {
                        this.createMarker(point);
                    }

                    this.panTo(point);
                });
            });

        template.html:
            {% load google_maps %}

            <!-- Статичная карта с зумом 15 размера 300x200 -->
            <img src='{{ address|google_map_static:"15,300,200" }}'>

            <!-- Ссылка на карту в сервисе Google -->
            <a href='{{ address|google_map_external:15 }}' target='_blank'>посмотреть карту</a>

            <!-- Интерактивная карта -->
            {% google_map_interactive address='Тольятти, Мира 6' zoom=14 height=300 %}
"""

from .api import geocode
from .models import geocode_cached
from .fields import GoogleCoordsField
from .widgets import GoogleCoordsFieldWidget

__all__ = ['geocode', 'geocode_cached', 'GoogleCoordsField', 'GoogleCoordsFieldWidget']