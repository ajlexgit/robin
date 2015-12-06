(function($) {

    /*
        Карта Google.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события GoogleMap.ready() или в onInit().

        1) Неявный GoogleMap.ready():
            var gmap = GoogleMap.create('#gmap');
            gmap.addPlacemark({
                lng: 49.418785,
                lat: 53.510171,
                hint: 'First',
                balloon: '<p>Hello</p>'
            });

        2) onInit():
            var gmap = GoogleMap.create('#gmap', {
                onInit: function() {
                    this.addPlacemark({
                        lng: 49.418785,
                        lat: 53.510171,
                        hint: 'First',
                        balloon: '<p>Hello</p>'
                    });

                    this.addPlacemark({
                        lng: 49.435000,
                        lat: 53.525000,
                        hint: 'second',
                        draggable: true,
                        balloon: '<p>Goodbay</p>'
                    });

                    this.setCenter(this.getPoints());
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


    var Placemark = Class(null, function Placemark(cls, superclass) {
        cls.prototype.init = function(gmap, options) {
            this.gmap = gmap;

            // настройки
            this.opts = $.extend({
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

                that.marker = that.gmap._createMarker(that.point, {
                    title: that.opts.hint,
                    draggable: that.opts.draggable
                });

                // клик на маркер
                that.gmap.addListener(that.marker, 'click', function() {
                    if (that.opts.onClick.call(that) === false) {
                        return
                    }

                    if (that.opts.balloon) {
                        that.gmap.balloon.setContent(that.opts.balloon);
                        that.gmap.balloon.open(that.gmap.map, that.marker);
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
        cls.prototype.setBalloon = function(content) {
            this.opts.balloon = content || '';
        };

        /*
            Перемещение маркера
         */
        cls.prototype.moveTo = function(point) {
            this.point = point;
            this.marker.setPosition(point);
        };
    });

    window.GoogleMap = Class(null, function GoogleMap(cls, superclass) {
        cls.prototype.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend(true, {
                lng: 49.418785,
                lat: 53.510171,
                map_options: {
                    disableDefaultUI: true,
                    zoomControl: true,
                    scrollwheel: false,
                    zoom: 15
                },
                onInit: $.noop,
                onResize: $.noop
            }, options);
            this.opts.lng = this.opts.lng || 49.418785;
            this.opts.lat = this.opts.lat || 53.510171;

            // точки на карте
            this.placemarks = [];

            var that = this;
            cls.ready(function() {
                // создание карты
                that.map = new google.maps.Map(
                    that.$root.get(0),
                    $.extend({
                        center: that.createPoint(that.opts.lng, that.opts.lat)
                    }, that.opts.map_options)
                );

                // Обработчик изменения размера экрана (например, для центрирования карты)
                google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                    that.opts.onResize.call(that);
                }, 300));


                // создание балуна
                that.balloon = that._createBalloon('');

                // callback
                that.opts.onInit.call(that);
            });

            this.$root.data(GoogleMap.dataParamName, this);
        };

        /*
            Выполнение callback, когда JS GoogleMaps загружен и готов
         */
        cls.ready = function(callback) {
            if (gmaps_ready) {
                callback()
            } else {
                $(document).one('google-maps-ready', callback);
            }
        };

        /*
            Создание маркера
         */
        cls.prototype._createMarker = function(point, options) {
            return new google.maps.Marker($.extend({}, options, {
                map: this.map,
                position: point
            }));
        };


        /*
            Создание балуна
         */
        cls.prototype._createBalloon = function(html) {
            if (html.jquery) {
                html = html.html();
            }

            return new google.maps.InfoWindow({
                content: html
            });
        };


        /*
            Получение координат текущего центра карты
         */
        cls.prototype.getCenter = function() {
            return this.map.getCenter()
        };


        /*
            Перемещение к точке или к множеству точек (bounds)
         */
        cls.prototype.setCenter = function(points) {
            if ($.isArray(points)) {
                this.map.fitBounds(boundsByPoints(points));
            } else {
                this.map.setCenter(points);
            }
        };


        /*
            Получение уровня приближения карты
         */
        cls.prototype.getZoom = function() {
            return this.map.getZoom()
        };


        /*
            Установка уровня приближения карты
         */
        cls.prototype.setZoom = function(zoom) {
            this.map.setZoom(zoom);
        };


        /*
            Плавное перемещение к точке
         */
        cls.prototype.panTo = function(point) {
            this.map.panTo(point);
        };


        /*
            Изменение опций карты
         */
        cls.prototype.setOptions = function(options) {
            this.map.setOptions(options);
        };


        /*
            Создание метки на карте
         */
        cls.prototype.addPlacemark = function(options) {
            var placemark = Placemark.create(this, options);
            if (placemark) {
                this.placemarks.push(placemark);
            }
            return placemark;
        };


        /*
            Получение метки на карте
         */
        cls.prototype.getPlacemark = function(index) {
            index = index || 0;
            return (this.placemarks.length > index) && this.placemarks[index];
        };


        /*
            Удаление метки на карте
         */
        cls.prototype.removePlacemark = function() {
            if (arguments[0] instanceof Placemark) {
                var index = this.placemarks.indexOf(arguments[0]);
            } else if (typeof index == 'number') {
                index = arguments[0];
            } else {
                return
            }

            if (this.placemarks.length > index) {
                var placemark = this.placemarks.splice(index, 1)[0];
                placemark.marker.setMap(null);
            }
        };

        /*
            Получение точек карты
         */
        cls.prototype.getPoints = function() {
            return this.placemarks.map(function(item) {
                return item.point
            })
        };

        /*
            Создание точки
         */
        cls.prototype.createPoint = function(lng, lat) {
            lng = parseFloat(lng.toString().replace(',', '.'));
            lat = parseFloat(lat.toString().replace(',', '.'));
            if (isNaN(lng) || isNaN(lat)) {
                return
            }
            return new google.maps.LatLng(lat, lng);
        };

        /*
            Добавление обработчика события на карте
         */
        cls.prototype.addListener = function(object, event, handler) {
            var that = this;
            google.maps.event.addListener(object, event, function() {
                return handler.apply(that, arguments);
            });
        };

        /*
            Получение координат по адресу.

            gmap.geocode('Тольятти Майский проезд 64', function(point) {
                this.addPlacemark({
                    point: point
                })
            }, function(status, results) {
                alert('Error:', status)
            })
         */
        cls.prototype.geocode = function(address, success, error) {
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
    });
    GoogleMap.dataParamName = 'map';

})(jQuery);
