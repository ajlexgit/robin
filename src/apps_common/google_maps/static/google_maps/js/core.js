(function($) {

    /*
        Карта Google.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события GoogleMaps.ready() или в onInit():
        1) GoogleMap.ready:
            var gmap = GoogleMap.create('#gmap');
            GoogleMap.ready(function() {
                var point = gmap.createPoint(49.418785, 53.510171);
                var marker = gmap.createMarker(point, {
                    draggable: true
                });
                var bubble = gmap.createBubble('<p>Hello</p>');
                gmap.addListener(marker, 'click', function() {
                    bubble.open(this.map, marker);
                });
            });

        2) onInit:
            var gmap = GoogleMap.create('#gmap', {
                onInit: function() {
                    this.points = [
                        this.createPoint(49.418785, 53.510171),
                        this.createPoint(49.435000, 53.525000)
                    ];

                    this.markers = [];
                    for(var i=0, l=this.points.length; i<l; i++) {
                        this.markers.push(this.createMarker(this.points[i]));
                    }

                    this.setCenter(this.points);
                }
            });


     */


    var gmaps_ready = false;
    window.init_google_maps = function() {
        gmaps_ready = true;
        $(document).trigger('google-maps-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');
        var script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&callback=init_google_maps&language=' + lang;
        document.body.appendChild(script);
    });


    /*
        Обертка над конструктором LatLngBounds, чтобы он принимал массив точек
     */
    var boundsByPoints = function(points) {
        function F() {
            return google.maps.LatLngBounds.apply(this, points);
        }

        F.prototype = google.maps.LatLngBounds.prototype;
        return new F();
    };


    window.GoogleMap = (function() {
        var GoogleMap = function() {};

        /*
            Выполнение callback, когда JS GoogleMaps загружен и готов
         */
        GoogleMap.ready = function(callback) {
            if (gmaps_ready) {
                callback()
            } else {
                $(document).on('google-maps-ready', callback);
            }
        };


        GoogleMap.create = function(container, options) {
            var self = new GoogleMap();

            self.$container = $.findFirstElement(container);
            if (!self.$container.length) {
                console.error('GoogleMap can\'t find container');
                return
            }

            // настройки
            self.opts = $.extend(true, self.getDefaultOpts(), options);
            self.opts.lng = self.opts.lng || 49.418785;
            self.opts.lat = self.opts.lat || 53.510171;

            GoogleMap.ready(function() {
                // создание карты
                self.map = new google.maps.Map(
                    self.$container.get(0),
                    $.extend({
                        center: self.createPoint(self.opts.lng, self.opts.lat)
                    }, self.opts.map_options)
                );

                // Обработчик изменения размера экрана (например, для центрирования карты)
                google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                    self.opts.onResize.call(self);
                }, 300));

                // callback
                self.opts.onInit.call(self);
            });

            self.$container.data('map', self);

            return self;
        };


        /*
            Настройки по умолчанию
         */
        GoogleMap.prototype.getDefaultOpts = function() {
            return {
                lng: 49.418785,
                lat: 53.510171,
                map_options: {
                    disableDefaultUI: true,
                    zoomControl: true,
                    scrollwheel: false,
                    zoom: 14
                },
                onInit: $.noop,
                onResize: $.noop
            }
        };


        /*
            Создание объекта точки GoogleMap
         */
        GoogleMap.prototype.createPoint = function(lng, lat) {
            lng = parseFloat(lng.toString().replace(',', '.'));
            lat = parseFloat(lat.toString().replace(',', '.'));
            if (isNaN(lng) || isNaN(lat)) {
                return
            }
            return new google.maps.LatLng(lat, lng);
        };


        /*
            Получение координат текущего центра карты
         */
        GoogleMap.prototype.getCenter = function() {
            return this.map.getCenter()
        };


        /*
            Перемещение к точке или к множеству точек (fitbounds)
         */
        GoogleMap.prototype.setCenter = function(points) {
            if ($.isArray(points)) {
                this.map.fitBounds(boundsByPoints(points));
            } else {
                this.map.setCenter(points);
            }
        };


        /*
            Изменение опций карты
         */
        GoogleMap.prototype.setOptions = function(options) {
            this.map.setOptions(options);
        };


        /*
            Создание маркера Google
         */
        GoogleMap.prototype.createMarker = function(point, options) {
            return new google.maps.Marker($.extend({}, options,{
                map: this.map,
                position: point
            }));
        };


        /*
            Создание всплывающей подсказки Google
         */
        GoogleMap.prototype.createBubble = function(html) {
            if (html.jquery) {
                html = html.html();
            }

            return new google.maps.InfoWindow({
                content: html
            });
        };


        /*
            Добавление обработчика события на карте
         */
        GoogleMap.prototype.addListener = function(object, event, handler) {
            var that = this;
            google.maps.event.addListener(object, event, function() {
                console.log(arguments);
                return handler.apply(that, arguments);
            });
        };


        /*
            Плавное перемещение к точке
         */
        GoogleMap.prototype.panTo = function(point) {
            this.map.panTo(point);
        };


        /*
            Получение координат по адресу.

            gmap.geocode('Тольятти Майский проезд 64', function(point) {
                this.createMarker(point)
            }, function(status, results) {
                alert('Error:', status)
            })
         */
        GoogleMap.prototype.geocode = function(address, success, error) {
            if (!this._geocoder) {
                this._geocoder = new google.maps.Geocoder();
            }

            var that = this;
            this._geocoder.geocode({
                address: address
            }, function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    success.call(that, results[0].geometry.location);
                } else {
                    error.call(that, status, results);
                }
            });
        };

        return GoogleMap;
    })();

})(jQuery);
