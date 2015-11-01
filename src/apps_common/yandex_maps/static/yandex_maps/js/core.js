(function($) {

    /*
        Карта Yandex.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события YandexMap.ready() или в onInit().

        1) Неявный YandexMap.ready():
            var ymap = YandexMap.create('#ymap');
            var mark = ymap.createPlacemark({
                lng: 49.418785,
                lat: 53.510171,
                hint: 'First',
                balloon: '<p>Hello</p>'
            });

        2) onInit():
            var ymap = YandexMap.create('#ymap', {
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


    var ymaps_ready = false;
    window.init_yandex_maps = function() {
        ymaps_ready = true;
        $(document).trigger('yandex-maps-ready');
    };

    $(document).ready(function() {
        var lang = $(document.documentElement).attr('lang');
        var script = document.createElement('script');
        script.src = '//api-maps.yandex.ru/2.1/?onload=init_yandex_maps&lang=' + lang;
        document.body.appendChild(script);
    });


    var Placemark = (function() {
        var Placemark = function(ymap, options) {
            this.ymap = ymap;

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
                    that.point = that.ymap.createPoint(that.opts.lng, that.opts.lat);
                }

                that.marker = that.ymap.createMarker(that.point, {
                    draggable: that.opts.draggable
                });
                that.marker.properties.set({
                    hintContent: that.opts.hint
                });

                // клик на маркер
                that.ymap.addListener(that.marker, 'click', function() {
                    if (that.opts.onClick.call(that) === false) {
                        return
                    }

                    if (that.opts.balloon) {
                        this.balloon.options.set({
                            contentLayout: ymaps.templateLayoutFactory.createClass(that.opts.balloon)
                        });
                        this.balloon.open(that.point);
                    }
                });

                // конец перетаскивания
                if (that.opts.draggable) {
                    that.ymap.addListener(that.marker, 'dragend', function() {
                        that.point = that.marker.geometry.getCoordinates();
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
            this.marker.geometry.setCoordinates(point);
        };

        /*
            Установка центра карты в этой точке
         */
        Placemark.prototype.center = function() {
            this.ymap.setCenter(this.point);
        };

        /*
            Перемещение центра карты в эту точку
         */
        Placemark.prototype.panHere = function() {
            this.ymap.panTo(this.point);
        };

        return Placemark;
    })();


    var map_index = 0;
    window.YandexMap = (function() {
        var YandexMap = function() {};

        /*
            Выполнение callback, когда JS YandexMaps загружен и готов
         */
        YandexMap.ready = function(callback) {
            if (ymaps_ready) {
                callback()
            } else {
                $(document).on('yandex-maps-ready', callback);
            }
        };


        YandexMap.create = function(container, options) {
            var self = new YandexMap();

            self.$container = $.findFirstElement(container);
            if (!self.$container.length) {
                console.error('YandexMap can\'t find container');
                return
            }

            var map_id = self.$container.attr('id');
            if (!map_id) {
                map_id = 'ymap_' + (++map_index);
            }
            self.$container.attr('id', map_id);

            // настройки
            self.opts = $.extend(true, self.getDefaultOpts(), options);
            self.opts.lng = self.opts.lng || 49.418785;
            self.opts.lat = self.opts.lat || 53.510171;

            YandexMap.ready(function() {
                // создание карты
                self.map = new ymaps.Map(map_id, $.extend({
                    center: self.createPoint(self.opts.lng, self.opts.lat)
                }, self.opts.map_options));

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
        YandexMap.prototype.getDefaultOpts = function() {
            return {
                lng: 49.418785,
                lat: 53.510171,
                map_options: {
                    controls: ["zoomControl", "fullscreenControl"],
                    zoom: 14
                },
                onInit: $.noop
            }
        };


        /*
            Получение координат текущего центра карты
         */
        YandexMap.prototype.getCenter = function() {
            return this.map.getCenter()
        };


        /*
            Перемещение к точке или к множеству точек (fitbounds)
         */
        YandexMap.prototype.setCenter = function(points) {
            if (points.length && $.isArray(points[0])) {
                this.map.setBounds(points, {
                    zoomMargin: 8
                });
            } else {
                this.map.setCenter(points);
            }
        };


        /*
            Изменение опций карты
         */
        YandexMap.prototype.setOptions = function(options) {
            this.map.setOptions(options);
        };


        /*
            Плавное перемещение к точке
         */
        YandexMap.prototype.panTo = function(point) {
            this.map.panTo(point);
        };


        /*
            Создание метки на карте.
         */
        YandexMap.prototype.createPlacemark = function(options) {
            return new Placemark(this, options);
        };


        /*
            Создание объекта точки YandexMap
         */
        YandexMap.prototype.createPoint = function(lng, lat) {
            lng = parseFloat(lng.toString().replace(',', '.'));
            lat = parseFloat(lat.toString().replace(',', '.'));
            if (isNaN(lng) || isNaN(lat)) {
                return
            }
            return [lat, lng];
        };


        /*
            Создание маркера
         */
        YandexMap.prototype.createMarker = function(point, options) {
            var marker = new ymaps.Placemark(point, {}, $.extend({}, options));
            this.map.geoObjects.add(marker);
            return marker;
        };


        /*
            Создание всплывающей подсказки
         */
        YandexMap.prototype.createBalloon = function(html) {
            if (html.jquery) {
                html = html.html();
            }

            var balloon = new ymaps.Balloon(this.map);
            balloon.options.setParent(this.map.options);
            balloon.options.set({
                contentLayout: ymaps.templateLayoutFactory.createClass(html)
            });

            return balloon;
        };


        /*
            Добавление обработчика события на карте
         */
        YandexMap.prototype.addListener = function(object, event, handler) {
            var that = this;
            object.events.add(event, function() {
                return handler.apply(that, arguments);
            });
        };


        /*
            Получение координат по адресу.

            ymap.geocode('Тольятти Майский проезд 64', function(point) {
                this.createMarker(point)
            }, function(err) {
                alert('Error:', err.message)
            })
         */
        YandexMap.prototype.geocode = function(address, success, error) {
            var that = this;
            ymaps.geocode(address, {results: 1}).then(function(results) {
                var point = results.geoObjects.get(0).geometry.getCoordinates();
                success.call(that, point);
            }, function(err) {
                error.call(that, err);
            });
        };

        return YandexMap;
    })();

})(jQuery);
