(function ($) {
    var map_index = 0;

    var YandexMap = function($map) {
        var that = this;
        var ymap_id = 'ymap_' + (++map_index);
        var map_data = $map.data();

        $map.attr('id', ymap_id);

        that.center = [
            parseFloat(map_data.lat) || 53.510171,
            parseFloat(map_data.lng) || 49.418785
        ];

        that.map = new ymaps.Map(ymap_id, {
            center: that.center,
            zoom: parseInt(map_data.zoom) || 14,
            type: 'yandex#publicMap',
            behaviors: ['default', 'scrollZoom']
        });

        that.map.controls.add('zoomControl');
        that.map.controls.add('mapTools');
        that.map.controls.add('typeSelector');

        that.marker = new ymaps.Placemark(that.center);
        that.map.geoObjects.add(that.marker);
    };

    window.init_yandex_maps = function() {
        $(document).trigger('yandex-maps-ready');
    };

    $(document).ready(function () {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = '//api-maps.yandex.ru/2.0-stable/?load=package.standard&onload=init_yandex_maps&lang=ru-RU';
        document.body.appendChild(script);
    }).on('yandex-maps-ready', function() {
        // Инициализация всех карт на странице
        $('.yandex-map').each(function() {
            var $this = $(this);
            $this.data('map', new YandexMap($this));
        });
    });

})(jQuery);
