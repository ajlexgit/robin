(function($) {
    /*var map_index = 0;

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
            behaviors: ['default', 'scrollZoom']
        });

        that.map.controls.add('zoomControl');
        that.map.controls.add('mapTools');
        that.map.controls.add('typeSelector');

        that.marker = new ymaps.Placemark(that.center);
        that.map.geoObjects.add(that.marker);
    };

    */


    /*
        Карта Yandex.

        Требует:
            jquery.utils.js
     */

    var map_index = 0;
    window.YandexMap = (function() {
        var YandexMap = function(container, options) {
            this.$container = $.findFirstElement(container);
            if (!this.$container.length) {
                console.error('GoogleMap can\'t find container');
                return
            }

            this.map_id = this.$container.attr('id');
            if (!this.map_id) {
                this.map_id = 'ymap_' + (++map_index);
                this.$container.attr('id', this.map_id);
            }

            // настройки
            this.opts = $.extend(true, this.getDefaultOpts(), options);
            this.opts.lng = this.opts.lng || 49.418785;
            this.opts.lat = this.opts.lat || 53.510171;

            // создание карты
            this.createMap(this.createPoint(this.opts.lng, this.opts.lat));

            this.$container.data('map', this);
        };

        YandexMap.prototype.getDefaultOpts = function() {
            return {
                lat: 53.510171,
                lng: 49.418785,
                zoom: 14
            }
        };

        // Создание точки Yandex
        YandexMap.prototype.createPoint = function(lng, lat) {
            lng = parseFloat(lng.toString().replace(',', '.'));
            lat = parseFloat(lat.toString().replace(',', '.'));
            if (isNaN(lng) || isNaN(lat)) {
                return
            }
            return [lat, lng];
        };

        // Создание карты Yandex
        YandexMap.prototype.createMap = function(arg1, arg2) {
            var point;
            if (arg1 instanceof Array) {
                point = arg1;
            } else {
                point = this.createPoint(arg1, arg2);
            }

            if (!point) {
                console.error('YandexMap: point is empty');
                return
            }

            this.map = new ymaps.Map(this.map_id, {
                center: point,
                zoom: this.opts.zoom,
                behaviors: ['default', 'scrollZoom']
            });

            this.map.controls.add('zoomControl');
            this.map.controls.add('mapTools');
            this.map.controls.add('typeSelector');
        };

        // Создание маркера Yandex
        YandexMap.prototype.createMarker = function(arg1, arg2) {
            if (!this.map) {
                console.error('YandexMap: map is empty');
                return
            }

            var point;
            if (arg1 instanceof Array) {
                point = arg1;
            } else {
                point = this.createPoint(arg1, arg2);
            }

            if (!point) {
                console.error('YandexMap: point is empty');
                return
            }

            var marker = new ymaps.Placemark(point);
            this.map.geoObjects.add(marker);
            return marker
        };

        // Создание всплывающей подсказки Google
        YandexMap.prototype.createBubble = function(html) {
            if (!html) {
                console.error('YandexMap: html is empty');
                return
            }

            if (html.jquery) {
                if (!html.length) {
                    console.error('YandexMap: html is empty');
                    return
                }

                html = html.html();
            }

            var bubble = new ymaps.Balloon(this.map);
            bubble.options.setParent(this.map.options);
            bubble.options.set({
                contentLayout: ymaps.templateLayoutFactory.createClass(html)
            });
            return bubble
        };

        // Перемещение к точке
        YandexMap.prototype.setCenter = function(arg1, arg2) {
            var point;
            if (arg1 instanceof google.maps.LatLng) {
                point = arg1;
            } else {
                point = this.createPoint(arg1, arg2);
            }

            if (!point) {
                console.error('YandexMap: point is empty');
                return
            }

            this.map.setCenter(point);
        };

        // Получение центра карты
        YandexMap.prototype.getCenter = function() {
            return this.map.getCenter()
        };

        return YandexMap;
    })();


    window.init_yandex_maps = function() {
        $(document).trigger('yandex-maps-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');
        var script = document.createElement('script');
        script.src = '//api-maps.yandex.ru/2.0-stable/?load=package.standard&onload=init_yandex_maps&lang=' + lang;
        document.body.appendChild(script);
    });

})(jQuery);
