from .api import geocode
from .models import geocode_cached
from .fields import YmapCoords, YmapCoordsField
from .widgets import YmapCoordsFieldWidget

"""
    Необходимо подключить скрипты:
        <script src="//api-maps.yandex.ru/2.0-stable/?load=package.standard&lang=ru-RU&onload=yaMapsCallback" async defer></script>
        yandex_maps/js/yandex_maps.js

    Настройки (settings.py):
        YANDEX_MAPS_API_KEY - ключ
        YANDEX_MAP_PERMISSIONS - функция определения прав на получение координат
                                 по адресу через AJAX (по умолчанию - сотрудники)
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
            from yandex_maps import YmapCoordsField
            ...

            address = models.CharField('адрес', max_length=255, blank=True)
            coords = YmapCoordsField('координаты',
                null=True,
                blank=True
            )

        Admin Javascript:
            // Получение координат по адресу в другом поле
            $(document).on('change', '#id_address', function() {
                var coords = $('#id_coords'),
                    map = coords.data('map');

                map.addressCoords( coords, $(this).val() );
            })

        template.html:
            {% load yandex_maps %}

            <!-- Статичная карта с зумом 15 размера 300x200 -->
            <img src='{{ address|static_map_url:"15,300,200" }}'>

            <!-- Ссылка на карту в сервисе Яндекса -->
            <a href='{{ address|external_map_url:15 }}' target='_blank'>посмотреть карту</a>

            <!-- Интерактивная карта -->
            {% interactive_map address='Тольятти, Мира 6' zoom=14 height=300 %}
"""
