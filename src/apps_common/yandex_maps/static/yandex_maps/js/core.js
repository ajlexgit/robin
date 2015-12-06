(function($) {

    /*
        Карта Yandex.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события YandexMap.ready() или в onInit().

        1) Неявный YandexMap.ready():
            var ymap = YandexMap.create('#ymap');
            ymap.addPlacemark({
                lng: 49.418785,
                lat: 53.510171,
                hint: 'First',
                balloon: '<p>Hello</p>'
            });

        2) onInit():
            var ymap = YandexMap.create('#ymap', {
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


    var Placemark = Class(null, function Placemark(cls, superclass) {
        cls.prototype.init = function(ymap, options) {
            this.ymap = ymap;

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
            YandexMap.ready(function() {
                if (that.opts.point) {
                    that.point = that.opts.point
                } else {
                    that.point = that.ymap.createPoint(that.opts.lng, that.opts.lat);
                }

                that.marker = that.ymap._createMarker(that.point, {
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
                        that.ymap.balloon.options.set({
                            contentLayout: ymaps.templateLayoutFactory.createClass(that.opts.balloon)
                        });
                        that.ymap.balloon.open(that.point);
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
        cls.prototype.setBalloon = function(content) {
            this.opts.balloon = content || '';
        };

        /*
            Перемещение маркера
         */
        cls.prototype.moveTo = function(point) {
            this.point = point;
            this.marker.geometry.setCoordinates(point);
        };
    });


    var map_index = 0;
    window.YandexMap = Class(null, function YandexMap(cls, superclass) {
        cls.prototype.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            var map_id = this.$root.attr('id');
            if (!map_id) {
                map_id = 'ymap_' + (++map_index);
            }
            this.$root.attr('id', map_id);

            // настройки
            this.opts = $.extend(true, {
                lng: 49.418785,
                lat: 53.510171,
                map_options: {
                    controls: ["zoomControl", "fullscreenControl"],
                    behaviors: ["drag", "dblClickZoom", "multiTouch"],
                    zoom: 15
                },
                onInit: $.noop
            }, options);
            this.opts.lng = this.opts.lng || 49.418785;
            this.opts.lat = this.opts.lat || 53.510171;

            // точки на карте
            this.placemarks = [];

            var that = this;
            YandexMap.ready(function() {
                // создание карты
                that.map = new ymaps.Map(map_id, $.extend({
                    center: that.createPoint(that.opts.lng, that.opts.lat)
                }, that.opts.map_options));

                // создание балуна
                that.balloon = that._createBalloon('');

                // callback
                that.opts.onInit.call(that);
            });

            this.$root.data(YandexMap.dataParamName, this);
        };

        /*
            Выполнение callback, когда JS YandexMaps загружен и готов
         */
        cls.ready = function(callback) {
            if (ymaps_ready) {
                callback()
            } else {
                $(document).one('yandex-maps-ready', callback);
            }
        };

        /*
            Создание маркера
         */
        cls.prototype._createMarker = function(point, options) {
            var marker = new ymaps.Placemark(point, {}, $.extend({}, options));
            this.map.geoObjects.add(marker);
            return marker;
        };

        /*
            Создание всплывающей подсказки
         */
        cls.prototype._createBalloon = function(html) {
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
            Получение координат текущего центра карты
         */
        cls.prototype.getCenter = function() {
            return this.map.getCenter()
        };

        /*
            Перемещение к точке или к множеству точек (bounds)
         */
        cls.prototype.setCenter = function(points) {
            if (points.length && $.isArray(points[0])) {
                this.map.setBounds(points, {
                    zoomMargin: 8
                });
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
            Создание метки на карте.
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
                this.map.geoObjects.remove(placemark.marker);
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
            Создание объекта точки YandexMap
         */
        cls.prototype.createPoint = function(lng, lat) {
            lng = parseFloat(lng.toString().replace(',', '.'));
            lat = parseFloat(lat.toString().replace(',', '.'));
            if (isNaN(lng) || isNaN(lat)) {
                return
            }
            return [lat, lng];
        };

        /*
            Добавление обработчика события на карте
         */
        cls.prototype.addListener = function(object, event, handler) {
            var that = this;
            object.events.add(event, function() {
                return handler.apply(that, arguments);
            });
        };

        /*
            Получение координат по адресу.

            ymap.geocode('Тольятти Майский проезд 64', function(point) {
                this.addPlacemark({
                    point: point
                })
            }, function(err) {
                alert('Error:', err.message)
            })
         */
        cls.prototype.geocode = function(address, success, error) {
            var that = this;
            ymaps.geocode(address, {results: 1}).then(function(results) {
                var point = results.geoObjects.get(0).geometry.getCoordinates();
                success.call(that, point);
            }, function(err) {
                error.call(that, err);
            });
        };
    });
    YandexMap.dataParamName = 'map';

})(jQuery);
