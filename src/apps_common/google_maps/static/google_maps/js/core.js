(function($) {
    'use strict';

    /*
        Карта Google.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события GMap.ready().

        Пример:
            var gmap = GMap('#gmap', {
                center: GMapPoint(53.510171, 49.418785),
                zoom: 2
            }).on('ready', function() {
                var marker1 = GMapMarker({
                    map: this,
                    position: GMapPoint(62.281819, -150.287132),
                    hint: 'First',
                    balloonContent: '<h1>Hello</h1>'
                }).on('click', function() {
                    // открытие окна при клике
                    this.openBalloon();
                });

                var marker2 = GMapMarker({
                    map: this,
                    position: GMapPoint(62.400471, -150.005608),
                    hint: 'second',
                    draggable: true
                });

                var overlay = GMapImageTripleOverlay({
                    map: this,
                    src: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/talkeetna.png',
                    coords: {
                        bottomleft: GMapPoint(62.281819, -150.287132),
                        topright: GMapPoint(62.400471, -150.005608)
                    }
                });

                // всплывающее окно
                this.balloon = GMapBalloon({
                    map: this
                });

                this.center(GMapPoint(62.339889, -150.145683));
            });
     */


    /*
        Базовый класс объекта на карте
     */
    window.GMapEventedObject = Class(EventedObject, function GMapEventedObject(cls, superclass) {
        cls.defaults = {};

        cls.NATIVE_EVENTS = [];


        cls.init = function(options) {
            superclass.init.call(this);

            this.opts = $.extend({}, this.defaults, options);

            // массив событий, которые повешены на нативный маркер
            this.native_events = [];

            // создание реального объекта GoogleMap
            var that = this;
            window.GMap.ready(function() {
                that.makeNative();
            });

            this.onInit();
        };

        /*
            Создание нативного объекта
         */
        cls.makeNative = function() {
            this.native = null;
        };

        /*
            Инициализация
         */
        cls.onInit = function() {

        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.native_events = [];
            superclass.destroy.call(this);
        };

        /*
            Отлов событий
         */
        cls._addEventHandler = function(name, handler, opts) {
            var evt_info = this._formatEventName(name);
            var evt_name = evt_info.name;
            if (evt_name &&
                (this.native_events.indexOf(evt_name) < 0) &&
                (this.NATIVE_EVENTS.indexOf(evt_name) >= 0)) {

                // вешаем обработчик на нативный маркер при первом обращении
                var that = this;
                window.GMap.ready(function() {
                    that.native_events.push(evt_name);
                    that.native.addListener(evt_name, function() {
                        var args = Array.prototype.slice.call(arguments);
                        args.unshift(evt_name);
                        that.trigger.apply(that, args);
                    });
                });
            }

            return superclass._addEventHandler.call(this, name, handler, opts);
        };
    });


    /*
        Базовый класс объекта на карте
     */
    window.GMapObject = Class(window.GMapEventedObject, function GMapObject(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            map: null
        });

        cls.NATIVE_EVENTS = [];


        /*
            Инициализация
         */
        cls.onInit = function() {
            superclass.onInit.call(this);
            this.map(this.opts.map);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.map(null);
            superclass.destroy.call(this);
        };

        /*
            Привязка к карте
         */
        cls._mapAttach = function() {
            this.native.setMap(this._map.native);
            this.trigger('attached');
            this._map.trigger('attach.overlay', this);
        };

        /*
            Отвязывание от карты
         */
        cls._mapDetach = function() {
            this._map.trigger('detach.overlay', this);
            this.trigger('detached');
            this.native.setMap(null);
        };

        /*
            Получение / установка карты
         */
        cls.map = function(value) {
            if (value === undefined) {
                // получение карты
                return this._map;
            }

            if (this._map) {
                if (value === this._map) {
                    // попытка подключения к текущей карте
                    return this;
                }

                // отключение от текущей карты
                this._mapDetach();
                this._map = null;
            }

            if (value !== null) {
                // подключение к новой карте
                if (value instanceof window.GMap == false) {
                    this.error('value should be a GMap instance');
                    return this;
                }

                this._map = value;
                this._mapAttach();
            }

            return this;
        };
    });


    /*
        Базовый класс наложения на карту Google.
     */
    window.GMapOverlayBase = Class(window.GMapObject, function GMapOverlayBase(cls, superclass) {
        cls.layer = 'overlayLayer';

        cls._nativeClass = function() {
            var native_class = new Function();
            native_class.prototype = new google.maps.OverlayView();

            var that = this;
            native_class.prototype.onAdd = function() {
                that.onAdd.call(that);
            };
            native_class.prototype.draw = function() {
                that.draw.call(that);
            };
            native_class.prototype.onRemove = function() {
                that.onRemove.call(that);
            };

            return native_class;
        };

        /*
            Создание нативного объекта
         */
        cls.makeNative = function() {
            var native_class = this._nativeClass();
            this.native = new native_class;
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.onAdd = function() {
            var panes = this.native.getPanes();
            panes[this.layer].appendChild(this.$container.get(0));
        };

        /*
            Отрисовка оверлея
         */
        cls.draw = function() {

        };

        /*
            Вызывается при откреплении оверлея от карты
         */
        cls.onRemove = function() {
            this.$container.remove();
            this.$container = null;
        };

        /*
            Привязка к карте
         */
        cls._mapAttach = function() {
            this.native.setMap(this._map.native);
            this.trigger('attached');
            this._map.trigger('attach.overlay', this);
        };

        /*
            Отвязывание от карты
         */
        cls._mapDetach = function() {
            this._map.trigger('detach.overlay', this);
            this.trigger('detached');
            this.native.setMap(null);
        };
    });


    /*
        Класс для пары координат
     */
    window.GMapPoint = Class(EventedObject, function GMapPoint(cls, superclass) {
        cls.init = function(lat, lng) {
            superclass.init.call(this);

            this.lat = this._formatCoord(lat);
            if (this.lat ===  false) {
                return this.raise('invalid latitude: ' + lat);
            }

            this.lng = this._formatCoord(lng);
            if (this.lng === false) {
                return this.raise('invalid longitude: ' + lng);
            }

            // нативный объект
            var that = this;
            window.GMap.ready(function() {
                that.native = new google.maps.LatLng(that.lat, that.lng);
            });
        };

        cls._formatCoord = function(value) {
            if (typeof value == 'string') {
                value = parseFloat(value.replace(',', '.'));
            }

            if ((typeof value == 'number') && !isNaN(value)) {
                return value;
            } else {
                return false;
            }
        };

        /*
            Превращение в строку "lat, lng"
         */
        cls.toString = function() {
            return [this.lat.toFixed(6), this.lng.toFixed(6)].join(', ');
        };
    });

    // =========================================
    //   Дополнительные конструкторы GMapPoint
    // =========================================

    // Создание объекта из строки "lat, lng"
    window.GMapPoint.fromString = function(str) {
        var coords = str.split(',');
        if (coords.length != 2) {
            console.error('invalid coords string: ' + str);
            return;
        }
        return this.create(coords[0], coords[1]);
    };

    // Создание объекта из нативного объекта
    window.GMapPoint.fromNative = function(native) {
        return this.create(native.lat(), native.lng());
    };


    /*
        Маркер на карте
     */
    window.GMapMarker = Class(window.GMapObject, function GMapMarker(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            position: null,
            icon: '',
            hint: '',
            draggable: false,
            balloonContent: ''
        });

        cls.NATIVE_EVENTS = [
            'click',
            'dblclick',
            'rightclick',
            'mousedown',
            'mouseup',
            'mouseover',
            'mouseout',
            'dragstart',
            'drag',
            'dragend',
            'position_changed',
            'draggable_changed',
            'icon_changed',
            'title_changed'
        ];


        /*
            Создание нативного объекта
         */
        cls.makeNative = function() {
            this.native = new google.maps.Marker();
        };

        cls.onInit = function() {
            superclass.onInit.call(this);
            this.position(this.opts.position);
            this.icon(this.opts.icon);
            this.hint(this.opts.hint);
            this.draggable(this.opts.draggable);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            google.maps.event.clearInstanceListeners(this.native);
            superclass.destroy.call(this);
        };

        /*
            Открытие окна, если оно есть
         */
        cls.openBalloon = function() {
            var map = this.map();
            if (!map.balloon) {
                return;
            }

            map.balloon.close();
            if (this.opts.balloonContent) {
                map.balloon.open(this);
            }

            if (map.balloon.content()) {
                map.balloon.open(this);
            }
        };

        /*
            Получение / установка положения
         */
        cls.position = function(value) {
            if (value === undefined) {
                // получение положения
                return window.GMapPoint.fromNative(this.native.getPosition());
            }

            if (value) {
                if (value instanceof window.GMapPoint == false) {
                    this.error('value should be a GMapPoint instance');
                    return this;
                }

                this.native.setPosition(value.native);
            }

            return this;
        };

        /*
            Получение / установка подсказки
         */
        cls.hint = function(value) {
            if (value === undefined) {
                // получение подсказки
                return this.native.getTitle();
            }

            if (value) {
                if (typeof value != 'string') {
                    this.error('value should be a string');
                    return this;
                }

                this.native.setTitle(value);
            }

            return this;
        };

        /*
            Получение / установка иконки
         */
        cls.icon = function(value) {
            if (value === undefined) {
                // получение иконки
                return this.native.getIcon();
            }

            if (value) {
                if ((typeof value != 'string') && (typeof value != 'object')) {
                    this.error('value should be a string or object');
                    return this;
                }

                this.native.setIcon(value);
            }

            return this;
        };

        /*
            Получение / установка возможности перетаскивания
         */
        cls.draggable = function(value) {
            if (value === undefined) {
                // получение значения
                return this.native.getDraggable();
            }

            this.native.setDraggable(Boolean(value));
            return this;
        };

        /*
            Привязка к карте
         */
        cls._mapAttach = function() {
            this.native.setMap(this._map.native);
            this.trigger('attached');
            this._map.trigger('attach.marker', this);
        };

        /*
            Отвязывание от карты
         */
        cls._mapDetach = function() {
            // закрытие балуна, если он привязан к этому маркеру
            if (this._map.balloon && (this._map.balloon._anchor == this)) {
                this._map.balloon.close();
            }

            this._map.trigger('detach.marker', this);
            this.trigger('detached');
            this.native.setMap(null);
        };
    });


    /*
        Класс карты Google
     */
    window.GMap = Class(window.GMapEventedObject, function GMap(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            center: null,
            mapType: 'roadmap',
            dblClickZoom: false,
            backgroundColor: '',
            draggable: true,
            wheel: false,
            noClear: false,
            styles: [
                {
                    "featureType": "poi",
                    "elementType": "labels.icon",
                    "stylers": [
                        {"visibility": "off"}
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "labels.icon",
                    "stylers": [
                        {"visibility": "off"}
                    ]
                },
                {
                    "featureType": "transit",
                    "elementType": "labels",
                    "stylers": [
                        {"visibility": "off"}
                    ]
                }
            ],
            zoom: 14,
            minZoom: null,
            maxZoom: null,
            zoomControl: true
        });

        cls.DATA_KEY = 'gmap';

        cls.NATIVE_EVENTS = [
            'click',
            'dblclick',
            'rightclick',
            'mouseover',
            'mousemove',
            'mouseout',
            'dragstart',
            'drag',
            'dragend',
            'idle',
            'center_changed',
            'zoom_changed'
        ];

        cls.MAP_TYPES = [
            'hybrid',
            'roadmap',
            'satellite',
            'terrain'
        ];


        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            superclass.init.call(this, options);
        };

        /*
            Создание нативного объекта
         */
        cls.makeNative = function() {
            this.native = new google.maps.Map(this.$root.get(0), {
                center: this.opts.center,
                noClear: this.opts.noClear,
                backgroundColor: this.opts.backgroundColor,
                disableDefaultUI: true
            });

            // Обработчик изменения размера экрана (например, для центрирования карты)
            var that = this;
            google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                that.trigger('resize');
            }, 300));

            this.draggable(this.opts.draggable);
            this.mapType(this.opts.mapType);
            this.wheel(this.opts.wheel);
            this.dblClickZoom(this.opts.dblClickZoom);
            this.styles(this.opts.styles);
            this.zoom(this.opts.zoom);
            this.maxZoom(this.opts.maxZoom);
            this.minZoom(this.opts.minZoom);
            this.zoomControl(this.opts.zoomControl);

            setTimeout(function() {
                that.trigger('ready');
            }, 0);
        };

        /*
            Инициализация
         */
        cls.onInit = function() {
            superclass.onInit.call(this);

            // маркеры на карте
            this.markers = [];
            this.on('attach.marker', function(marker) {
                // добавление маркера в массив
                this.markers.push(marker);
            }).on('detach.marker', function(marker) {
                // удаление маркера из массива
                var index = this.markers.indexOf(marker);
                if (index >= 0) {
                    this.markers.splice(index, 1);
                }
            });

            // оверлеи на карте
            this.overlays = [];
            this.on('attach.overlay', function(overlay) {
                // добавление оверлея в массив
                this.overlays.push(overlay);
            }).on('detach.overlay', function(overlay) {
                // удаление оверлея из массива
                var index = this.overlays.indexOf(overlay);
                if (index >= 0) {
                    this.overlays.splice(index, 1);
                }
            });

            // Не даём скроллить слишком далеко по вертикали
            var MAX_LATITUDE = 83.675733;
            var MIN_LATITUDE = -85.0511287798;
            var AMPLITUDE = 2;
            this.on('idle', function() {
                var center = this.center();
                if (center.lat < (MIN_LATITUDE - AMPLITUDE)) {
                    this.panTo(window.GMapPoint(MIN_LATITUDE, center.lng), 100);
                } else if (center.lat > (MAX_LATITUDE + AMPLITUDE)) {
                    this.panTo(window.GMapPoint(MAX_LATITUDE, center.lng), 100);
                }
            });

            this.$root.data(this.DATA_KEY, this);
        };

        /*
            Получение / установка центра карты
         */
        cls.center = function(value) {
            if (value === undefined) {
                // получение центра карты
                return window.GMapPoint.fromNative(this.native.getCenter());
            }

            if (value) {
                if (value instanceof window.GMapMarker) {
                    this.native.setCenter(value.position().native);
                } else if (value instanceof window.GMapPoint) {
                    this.native.setCenter(value.native);
                } else {
                    this.error('value should be a GMapPoint or GMapMarker instance');
                }
            }

            return this;
        };

        /*
            Получение / установка возможности перетаскивания карты
         */
        cls.draggable = function(value) {
            if (value === undefined) {
                // получение значения
                return this.native.draggable;
            }

            this.native.setOptions({
                draggable: Boolean(value)
            });

            return this;
        };

        /*
            Плавное перемещение к точке
         */
        cls.panTo = function(center) {
            if (center instanceof window.GMapMarker) {
                var target = center.position();
            } else if (center instanceof window.GMapPoint) {
                target = center;
            } else {
                this.error('value should be a GMapPoint or GMapMarker instance');
                return;
            }

            this.native.panTo(target.native);
        };

        /*
            Смещение центра на заданное расстояние
         */
        cls.panBy = function(dx, dy) {
            dx = parseFloat(dx);
            dy = parseFloat(dy);

            if (isNaN(dx)) {
                this.raise('dx should be a number');
            }
            if (isNaN(dy)) {
                this.raise('dy should be a number');
            }

            this.native.panBy(dx, dy);
        };

        /*
            Получение / установка зума карты через колесико
         */
        cls.wheel = function(value) {
            if (value === undefined) {
                // получение значения
                return this.native.scrollwheel;
            }

            this.native.setOptions({
                scrollwheel: Boolean(value)
            });

            return this;
        };

        /*
            Получение / установка разрешения на зум через двойной клик
         */
        cls.dblClickZoom = function(value) {
            if (value === undefined) {
                // получение значения
                return !this.native.disableDoubleClickZoom;
            }

            this.native.setOptions({
                disableDoubleClickZoom: !Boolean(value)
            });

            return this;
        };

        /*
            Получение / установка типа карты
         */
        cls.mapType = function(value) {
            if (value === undefined) {
                // получение значения
                return this.native.native.getMapTypeId();
            }

            value = value.toLowerCase();
            if (this.MAP_TYPES.indexOf(value) < 0) {
                this.error('unknown map type: ' + value);
                return this;
            }

            this.native.setMapTypeId(value);
            return this;
        };

        /*
            Получение / установка стилей карты
         */
        cls.styles = function(value) {
            if (value === undefined) {
                // получение значения
                return this.native.get('styles');
            }

            if (value && !$.isArray(value)) {
                this.error('value should be an array');
                return this;
            }

            this.native.set('styles', value);
            return this;
        };

        /*
            Получение / установка зума карты
         */
        cls.zoom = function(value) {
            if (value === undefined) {
                // получение зума
                return this.native.getZoom();
            }

            if (value && (typeof value != 'number')) {
                this.error('value should be a number');
                return this;
            }

            this.native.setZoom(value);
            return this;
        };

        /*
            Получение / установка максимального зума карты
         */
        cls.maxZoom = function(value) {
            if (value === undefined) {
                // получение зума
                return this._maxZoom;
            }

            if (value && (typeof value != 'number') && (value !== null)) {
                this.error('value should be a number or null');
                return this;
            }

            this._maxZoom = value;
            if (this._maxZoom) {
                var that = this;
                this.on('zoom_changed.maxzoom', function() {
                    var currentZoom = that.zoom();
                    if (currentZoom > that._maxZoom) {
                        that.zoom(that._maxZoom);
                    }
                });

                var currentZoom = this.zoom();
                if (currentZoom > this._maxZoom) {
                    this.zoom(this._maxZoom);
                }
            } else {
                this.off('zoom_changed.maxzoom');
            }

            return this;
        };

        /*
            Получение / установка минимального зума карты
         */
        cls.minZoom = function(value) {
            if (value === undefined) {
                // получение зума
                return this._minZoom;
            }

            if (value && (typeof value != 'number') && (value !== null)) {
                this.error('value should be a number or null');
                return this;
            }

            this._minZoom = value;
            if (this._minZoom) {
                var that = this;
                this.on('zoom_changed.minzoom', function() {
                    var currentZoom = that.zoom();
                    if (currentZoom < that._minZoom) {
                        that.zoom(that._minZoom);
                    }
                });

                var currentZoom = this.zoom();
                if (currentZoom < this._minZoom) {
                    this.zoom(this._minZoom);
                }
            } else {
                this.off('zoom_changed.minzoom');
            }

            return this;
        };

        /*
            Получение / установка наличия зума карты
         */
        cls.zoomControl = function(value) {
            if (value === undefined) {
                // получение значения
                return this.native.zoomControl;
            }

            this.native.setOptions({
                zoomControl: Boolean(value)
            });

            return this;
        };

        /*
            Авторасчет зума и центра, чтобы были видны маркеры
         */
        cls.fitBounds = function() {
            var bounds = new google.maps.LatLngBounds();

            var items = arguments.length ? arguments : this.markers;
            $.each(items, function(i, item) {
                if (item instanceof window.GMapPoint) {
                    bounds.extend(item.native);
                } else if (item instanceof window.GMapMarker) {
                    bounds.extend(item.position().native);
                }
            });

            this.native.fitBounds(bounds);
        };

        /*
            Удаление всех маркеров
         */
        cls.removeAllMarkers = function() {
            var marker;
            while (marker = this.markers[0]) {
                marker.destroy();
            }
        };

        /*
            Удаление всех оверлеев
         */
        cls.removeAllOverlays = function() {
            var overlay;
            while (overlay = this.overlays[0]) {
                overlay.destroy();
            }
        };

        /*
            Получение координат по адресу.

            gmap.geocode('Тольятти Майский проезд 64', function(point) {
                GMapMarker({
                    map: this,
                    position: point
                })
            }, function(status, results) {
                alert('Error:', status)
            })
         */
        cls.geocode = function(address, success, error) {
            if (!this._geocoder) {
                this._geocoder = new google.maps.Geocoder();
            }

            var that = this;
            this._geocoder.geocode({
                address: address
            }, function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    var native_point = results[0].geometry.location;
                    success.call(that, window.GMapPoint.fromNative(native_point));
                } else if ($.isFunction(error)) {
                    error.call(that, status, results);
                }
            });
        };
    });


    var gmaps_ready = false;
    window.init_google_maps = function() {
        gmaps_ready = true;
        $(document).trigger('google-maps-ready');
    };

    $(document).ready(function() {
        var lang = document.documentElement.getAttribute('lang');
        var script = document.createElement('script');
        script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&callback=init_google_maps&libraries=places&language=' + lang;
        document.body.appendChild(script);
    });

    /*
        Выполнение callback, когда JS GoogleMaps загружен и готов
     */
    window.GMap.ready = function(callback) {
        if (gmaps_ready) {
            callback()
        } else {
            $(document).one('google-maps-ready', callback);
        }
    };

})(jQuery);
