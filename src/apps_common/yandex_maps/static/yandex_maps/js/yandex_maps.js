(function ($) {
    var map_index = 0;

    window.init_yandex_map = function() {
        // Инициализация одной карты
        var ymap_id = 'ymap_'+(++map_index),
            ymap_div = $(this).attr('id', ymap_id),
            ymap_div_data = ymap_div.data();

        ymaps.ready(function () {
            var center = [
                    parseFloat(ymap_div_data.lat) || 53.510171,
                    parseFloat(ymap_div_data.lng) || 49.418785
                ],
                myPoint;

            var map = new ymaps.Map(ymap_id, {
                center: center,
                zoom: parseInt(ymap_div_data.zoom) || 14,
                type: 'yandex#publicMap',
                behaviors: ['default', 'scrollZoom']
            });

            map.controls.add('zoomControl');
            map.controls.add('mapTools');
            map.controls.add('typeSelector');

            if (ymap_div_data.header || ymap_div_data.content) {
                myPoint = new ymaps.Placemark(center, {
                    balloonContentHeader: ymap_div_data.header,
                    balloonContentBody: ymap_div_data.content
                })
            } else {
                myPoint = new ymaps.Placemark(center);
            }
            map.geoObjects.add(myPoint);
        });
    };

    window.init_yandex_maps = function() {
        // Инициализация всех карт на странице
        $('.yandex-map').each(window.init_yandex_map);
    };

    $(document).ready(function () {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = '//api-maps.yandex.ru/2.0-stable/?load=package.standard&onload=init_yandex_maps&lang=ru-RU';
        document.body.appendChild(script);
    });

})(jQuery);
