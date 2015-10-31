(function($) {

    /*
        Карта Yandex.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события YandexMap.ready() или в onInit():
        1) YandexMap.ready:
            var ymap = YandexMap.create('#ymap');
            YandexMap.ready(function() {
                var point = ymap.createPoint(49.418785, 53.510171);
                var marker = ymap.createMarker(point, {
                    draggable: true
                });
                var bubble = ymap.createBubble('<p>Hello</p>');
                ymap.addListener(marker, 'click', function() {
                    bubble.open(marker.geometry.getCoordinates());
                });
            });

        2) onInit:
            var ymap = YandexMap.create('#ymap', {
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
        YandexMap.prototype.createBubble = function(html) {
            if (html.jquery) {
                html = html.html();
            }

            var bubble = new ymaps.Balloon(this.map);
            bubble.options.setParent(this.map.options);
            bubble.options.set({
                contentLayout: ymaps.templateLayoutFactory.createClass(html)
            });

            return bubble;
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
            Плавное перемещение к точке
         */
        YandexMap.prototype.panTo = function(point) {
            this.map.panTo(point);
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
