(function($) {

    /*
        Карта Google.

        Требует:
            jquery.utils.js
     */

    window.GoogleMap = (function() {
        var GoogleMap = function(container, options) {
            this.$container = $.findFirstElement(container);
            if (!this.$container.length) {
                console.error('GoogleMap can\'t find container');
                return
            }

            // настройки
            this.opts = $.extend(true, this.getDefaultOpts(), options);
            this.opts.lng = this.opts.lng || 49.418785;
            this.opts.lat = this.opts.lat || 53.510171;

            // создание карты
            this.createMap(this.createPoint(this.opts.lng, this.opts.lat));

            // Изменение размера экрана
            var that = this;
            google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                that.opts.onResize.call(that);
            }, 300));

            this.$container.data('map', this);
        };

        GoogleMap.prototype.getDefaultOpts = function() {
            return {
                lat: 53.510171,
                lng: 49.418785,
                zoom: 14,
                onResize: $.noop
            }
        };

        // Создание точки Google
        GoogleMap.prototype.createPoint = function(lng, lat) {
            lng = parseFloat(lng.toString().replace(',', '.'));
            lat = parseFloat(lat.toString().replace(',', '.'));
            if (isNaN(lng) || isNaN(lat)) {
                return
            }
            return new google.maps.LatLng(lat, lng);
        };

        // Создание карты Google
        GoogleMap.prototype.createMap = function(arg1, arg2) {
            var point;
            if (arg1 instanceof google.maps.LatLng) {
                point = arg1;
            } else {
                point = this.createPoint(arg1, arg2);
            }

            if (!point) {
                console.error('GoogleMap: point is empty');
                return
            }

            this.map = new google.maps.Map(this.$container.get(0), {
                zoom: this.opts.zoom,
                center: point
            });
        };

        // Создание маркера Google
        GoogleMap.prototype.createMarker = function(arg1, arg2) {
            if (!this.map) {
                console.error('GoogleMap: map is empty');
                return
            }

            var point;
            if (arg1 instanceof google.maps.LatLng) {
                point = arg1;
            } else {
                point = this.createPoint(arg1, arg2);
            }

            if (!point) {
                console.error('GoogleMap: point is empty');
                return
            }

            return new google.maps.Marker({
                map: this.map,
                position: point
            });
        };

        // Создание всплывающей подсказки Google
        GoogleMap.prototype.createBubble = function(html) {
            if (!html) {
                console.error('GoogleMap: html is empty');
                return
            }

            if (html.jquery) {
                if (!html.length) {
                    console.error('GoogleMap: html is empty');
                    return
                }

                html = html.html();
            }

            return new google.maps.InfoWindow({
                content: html
            });
        };

        // Перемещение к точке
        GoogleMap.prototype.setCenter = function(arg1, arg2) {
            var point;
            if (arg1 instanceof google.maps.LatLng) {
                point = arg1;
            } else {
                point = this.createPoint(arg1, arg2);
            }

            if (!point) {
                console.error('GoogleMap: point is empty');
                return
            }

            this.map.setCenter(point);
        };

        // Получение центра карты
        GoogleMap.prototype.getCenter = function() {
            return this.map.getCenter()
        };

        return GoogleMap;
    })();


    window.init_google_maps = function() {
        $(document).trigger('google-maps-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');
        var script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&callback=init_google_maps&language=' + lang;
        document.body.appendChild(script);
    });

})(jQuery);
