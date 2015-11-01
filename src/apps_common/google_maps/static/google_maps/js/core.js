(function($) {

    /*
        Карта Google.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события GoogleMaps.ready() или в onInit().

        1) Неявный GoogleMap.ready():
            var gmap = GoogleMap.create('#gmap');
            var mark = gmap.createPlacemark({
                lng: 49.418785,
                lat: 53.510171,
                hint: 'First',
                balloon: '<p>Hello</p>'
            });

        2) onInit():
            var gmap = GoogleMap.create('#gmap', {
                onInit: function() {
                    this.placemarks = [
                        this.createPlacemark({
                            lng: 49.418785,
                            lat: 53.510171,
                            hint: 'First',
                            balloon: '<p>Hello</p>'
                        }),
                        this.createPlacemark({
                            lng: 49.435000,
                            lat: 53.525000,
                            hint: 'second',
                            draggable: true,
                            balloon: '<p>Goodbay</p>'
                        })
                    ];

                    this.setCenter(this.placemarks.map(function(item) {
                        return item.point
                    }));
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


    var Placemark = (function() {
        var Placemark = function(gmap, options) {
            this.gmap = gmap;

            this.opts = $.extend(true, {
                lng: 49.418785,
                lat: 53.510171,
                point: null,
                draggable: false,
                hint: '',
                balloon: '',
                onClick: $.noop,
                onDragEnd: $.noop
            }, options);

            var that = this;
            GoogleMap.ready(function() {
                if (that.opts.point) {
                    that.point = that.opts.point
                } else {
                    that.point = that.gmap.createPoint(that.opts.lng, that.opts.lat);
                }

                that.marker = that.gmap.createMarker(that.point, {
                    title: that.opts.hint,
                    draggable: that.opts.draggable
                });

                // клик на маркер
                that.gmap.addListener(that.marker, 'click', function() {
                    if (that.opts.onClick.call(that) === false) {
                        return
                    }

                    if (that.opts.balloon) {
                        this.balloon.setContent(that.opts.balloon);
                        this.balloon.open(this.map, that.marker);
                    }
                });

                // конец перетаскивания
                if (that.opts.draggable) {
                    that.gmap.addListener(that.marker, 'dragend', function() {
                        that.point = that.marker.getPosition();
                        that.opts.onDragEnd.call(that);
                    });
                }
            });
        };

        /*
            Установка текста балуна
         */
        Placemark.prototype.setBalloon = function(content) {
            this.opts.balloon = content || '';
        };

        /*
            Перемещение маркера
         */
        Placemark.prototype.moveTo = function(point) {
            this.point = point;
            this.marker.setPosition(point);
        };

        /*
            Установка центра карты в этой точке
         */
        Placemark.prototype.center = function() {
            this.gmap.setCenter(this.point);
        };

        /*
            Перемещение центра карты в эту точку
         */
        Placemark.prototype.panHere = function() {
            this.gmap.panTo(this.point);
        };

        return Placemark;
    })();


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


                // создание балуна
                self.balloon = self.createBalloon('');

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
            Плавное перемещение к точке
         */
        GoogleMap.prototype.panTo = function(point) {
            this.map.panTo(point);
        };


        /*
            Создание метки на карте.
         */
        GoogleMap.prototype.createPlacemark = function(options) {
            return new Placemark(this, options);
        };


        /*
            Создание точки
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
            Создание маркера
         */
        GoogleMap.prototype.createMarker = function(point, options) {
            return new google.maps.Marker($.extend({}, options,{
                map: this.map,
                position: point
            }));
        };


        /*
            Создание балуна
         */
        GoogleMap.prototype.createBalloon = function(html) {
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
                return handler.apply(that, arguments);
            });
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
