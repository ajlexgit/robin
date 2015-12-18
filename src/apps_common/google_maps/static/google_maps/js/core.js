(function($) {

    /*
        Карта Google.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события GMap.ready().

        Пример:
            var gmap = GMap('#gmap', {
                center: GMapPoint(53.510171, 49.418785),
                styles: gmapStyles,
                zoom: 2
            }).on('ready', function() {
                var marker1 = GMapMarker({
                    map: this,
                    position: GMapPoint(62.281819, -150.287132),
                    hint: 'First',
                    balloonContent: '<h1>Hello</h1>'
                }).on('click', function() {
                    // открытие окна при клике
                    var map = this.map();
                    if (!map.balloon) {
                        return;
                    }

                    map.balloon.close();
                    if (this.opts.balloonContent) {
                        map.balloon.content(this.opts.balloonContent);
                        map.balloon.open(this);
                    }
                });;

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
        Базовый класс объекта на карте
     */
    window.GMapEventedObject = Class(EventedObject, function GMapPoint(cls, superclass) {
        cls.prototype.NATIVE_EVENTS = [];

        cls.prototype.init = function(options) {
            superclass.prototype.init.call(this);

            this.opts = $.extend(this.getDefaultOpts(), options);

            // массив событий, которые повешены на нативный маркер
            this.native_events = [];

            // создание реального объекта GoogleMap
            var that = this;
            GMap.ready(function() {
                that.makeNative();
            });

            this.onInit();
        };

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return {}
        };

        /*
            Создание нативного объекта
         */
        cls.prototype.makeNative = function() {
            this.native = null;
        };

        /*
            Инициализация
         */
        cls.prototype.onInit = function() {

        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            this.native_events = [];
            superclass.prototype.destroy.call(this);
        };

        /*
            Отлов событий
         */
        cls.prototype._addEventHandler = function(name, handler, opts) {
            var evt_info = this._formatEventName(name);
            var evt_name = evt_info.name;
            if (evt_name &&
                (this.native_events.indexOf(evt_name) < 0) &&
                (this.NATIVE_EVENTS.indexOf(evt_name) >= 0)) {

                // вешаем обработчик на нативный маркер при первом обращении
                var that = this;
                GMap.ready(function() {
                    that.native_events.push(evt_name);
                    that.native.addListener(evt_name, function() {
                        that.trigger(evt_name, arguments);
                    });
                });
            }

            return superclass.prototype._addEventHandler.call(this, name, handler, opts);
        };
    });


    /*
        Базовый класс объекта на карте
     */
    window.GMapObject = Class(GMapEventedObject, function GMapPoint(cls, superclass) {
        cls.prototype.NATIVE_EVENTS = [];

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                map: null
            });
        };

        /*
            Инициализация
         */
        cls.prototype.onInit = function() {
            superclass.prototype.onInit.call(this);
            this.map(this.opts.map);
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            this.map(null);
            superclass.prototype.destroy.call(this);
        };

        /*
            Привязка к карте
         */
        cls.prototype._mapAttach = function() {
            this.native.setMap(this._map.native);
            this.trigger('attached');
            this._map.trigger('attach.overlay', this);
        };

        /*
            Отвязывание от карты
         */
        cls.prototype._mapDetach = function() {
            this._map.trigger('detach.overlay', this);
            this.trigger('detached');
            this.native.setMap(null);
        };

        /*
            Получение / установка карты
         */
        cls.prototype.map = function(value) {
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
                if (value instanceof GMap == false) {
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
    window.GMapOverlayBase = Class(GMapObject, function GMapOverlayBase(cls, superclass) {
        cls.prototype.layer = 'overlayLayer';

        cls.prototype._nativeClass = function() {
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
        cls.prototype.makeNative = function() {
            var native_class = this._nativeClass();
            this.native = new native_class;
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.prototype.onAdd = function() {
            var panes = this.native.getPanes();
            panes[this.layer].appendChild(this.$container.get(0));
        };

        /*
            Отрисовка оверлея
         */
        cls.prototype.draw = function() {

        };

        /*
            Вызывается при откреплении оверлея от карты
         */
        cls.prototype.onRemove = function() {
            this.$container.remove();
            this.$container = null;
        };

        /*
            Привязка к карте
         */
        cls.prototype._mapAttach = function() {
            this.native.setMap(this._map.native);
            this.trigger('attached');
            this._map.trigger('attach.overlay', this);
        };

        /*
            Отвязывание от карты
         */
        cls.prototype._mapDetach = function() {
            this._map.trigger('detach.overlay', this);
            this.trigger('detached');
            this.native.setMap(null);
        };
    });


    /*
        Класс для пары координат
     */
    window.GMapPoint = Class(EventedObject, function GMapPoint(cls, superclass) {
        cls.prototype.init = function(lat, lng) {
            superclass.prototype.init.call(this);

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
            GMap.ready(function() {
                that.native = new google.maps.LatLng(that.lat, that.lng);
            });
        };

        cls.prototype._formatCoord = function(value) {
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
        cls.prototype.toString = function() {
            return [this.lat.toFixed(6), this.lng.toFixed(6)].join(', ');
        };

        /*
            Создание объекта из строки "lat, lng"
         */
        cls.fromString = function(str) {
            var coords = str.toString().split(',');
            if (coords.length != 2) {
                console.error('invalid coords string: ' + str);
                return;
            }
            return cls.create(coords[0], coords[1]);
        };

        /*
            Создание объекта из нативного объекта
         */
        cls.fromNative = function(native) {
            return cls.create(native.lat(), native.lng());
        }
    });


    /*
        Маркер на карте
     */
    window.GMapMarker = Class(GMapObject, function GMapMarker(cls, superclass) {
        cls.prototype.NATIVE_EVENTS = [
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
        cls.prototype.makeNative = function() {
            this.native = new google.maps.Marker();
        };

        cls.prototype.onInit = function() {
            superclass.prototype.onInit.call(this);
            this.position(this.opts.position);
            this.icon(this.opts.icon);
            this.hint(this.opts.hint);
            this.draggable(this.opts.draggable);
        };

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                position: null,
                icon: '',
                hint: '',
                draggable: false
            });
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            google.maps.event.clearInstanceListeners(this.native);
            superclass.prototype.destroy.call(this);
        };

        /*
            Получение / установка положения
         */
        cls.prototype.position = function(value) {
            if (value === undefined) {
                // получение положения
                return GMapPoint.fromNative(this.native.getPosition());
            }

            if (value) {
                if (value instanceof GMapPoint == false) {
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
        cls.prototype.hint = function(value) {
            if (value === undefined) {
                // получение подсказки
                return this.native.getTitle();
            }

            if (value && (typeof value != 'string')) {
                this.error('value should be a string');
                return this;
            }

            this.native.setTitle(value);
            return this;
        };

        /*
            Получение / установка иконки
         */
        cls.prototype.icon = function(value) {
            if (value === undefined) {
                // получение иконки
                return this.native.getIcon();
            }

            if (value && (typeof value != 'string') && (typeof value != 'object')) {
                this.error('value should be a string or object');
                return this;
            }

            this.native.setIcon(value);
            return this;
        };

        /*
            Получение / установка возможности перетаскивания
         */
        cls.prototype.draggable = function(value) {
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
        cls.prototype._mapAttach = function() {
            this.native.setMap(this._map.native);
            this.trigger('attached');
            this._map.trigger('attach.marker', this);
        };

        /*
            Отвязывание от карты
         */
        cls.prototype._mapDetach = function() {
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
    window.GMap = Class(GMapEventedObject, function GMap(cls, superclass) {
        cls.prototype.NATIVE_EVENTS = [
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

        cls.prototype.MAP_TYPES = [
            'hybrid',
            'roadmap',
            'satellite',
            'terrain'
        ];

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

        cls.prototype.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            superclass.prototype.init.call(this, options);
        };

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                center: null,
                mapType: 'roadmap',
                dblClickZoom: false,
                backgroundColor: '',
                draggable: true,
                wheel: false,
                noClear: false,
                styles: [],
                zoom: 14,
                zoomControl: true
            });
        };

        /*
            Создание нативного объекта
         */
        cls.prototype.makeNative = function() {
            this.native = new google.maps.Map(this.$root.get(0), {
                center: this.opts.center,
                noClear: this.opts.noClear,
                backgroundColor: this.opts.backgroundColor,
                disableDoubleClickZoom: !this.opts.dblClickZoom,
                disableDefaultUI: true,
                zoomControl: this.opts.zoomControl
            });

            // Обработчик изменения размера экрана (например, для центрирования карты)
            var that = this;
            google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                that.trigger('resize');
            }, 300));

            this.draggable(this.opts.draggable);
            this.mapType(this.opts.mapType);
            this.wheel(this.opts.wheel);
            this.styles(this.opts.styles);
            this.zoom(this.opts.zoom);

            setTimeout(function() {
                that.trigger('ready');
            }, 0);
        };

        /*
            Инициализация
         */
        cls.prototype.onInit = function() {
            superclass.prototype.onInit.call(this);

            // маркеры на карте
            this.markers = [];
            this.on('attach.marker', function(e, marker) {
                // добавление маркера в массив
                this.markers.push(marker);
            }).on('detach.marker', function(e, marker) {
                // удаление маркера из массива
                var index = this.markers.indexOf(marker);
                if (index >= 0) {
                    this.markers.splice(index, 1);
                }
            });

            // оверлеи на карте
            this.overlays = [];
            this.on('attach.overlay', function(e, overlay) {
                // добавление оверлея в массив
                this.overlays.push(overlay);
            }).on('detach.overlay', function(e, overlay) {
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
                    this.panTo(GMapPoint(MIN_LATITUDE, center.lng), 100);
                } else if (center.lat > (MAX_LATITUDE + AMPLITUDE)) {
                    this.panTo(GMapPoint(MAX_LATITUDE, center.lng), 100);
                }
            });

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Получение / установка центра карты
         */
        cls.prototype.center = function(value) {
            if (value === undefined) {
                // получение центра карты
                return GMapPoint.fromNative(this.native.getCenter());
            }

            if (value) {
                if (value instanceof GMapMarker) {
                    this.native.setCenter(value.position().native);
                } else if (value instanceof GMapPoint) {
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
        cls.prototype.draggable = function(value) {
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
        cls.prototype.panTo = function(center, speed) {
            speed = parseInt(speed) || 500;

            if (center instanceof GMapMarker) {
                var target = center.position();
            } else if (center instanceof GMapPoint) {
                target = center;
            } else {
                this.error('value should be a GMapPoint or GMapMarker instance');
                return;
            }

            this.native.panTo(target.native);
        };

        /*
            Получение / установка зума карты через колесико
         */
        cls.prototype.wheel = function(value) {
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
            Получение / установка типа карты
         */
        cls.prototype.mapType = function(value) {
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
        cls.prototype.styles = function(value) {
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
        cls.prototype.zoom = function(value) {
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
            Авторасчет зума и центра, чтобы были видны маркеры
         */
        cls.prototype.fitBounds = function() {
            var bounds = new google.maps.LatLngBounds();

            var items = arguments.length ? arguments : this.markers;
            $.each(items, function(i, item) {
                if (item instanceof GMapPoint) {
                    bounds.extend(item.native);
                } else if (item instanceof GMapMarker) {
                    bounds.extend(item.position().native);
                }
            });

            this.native.fitBounds(bounds);
        };

        /*
            Удаление всех маркеров
         */
        cls.prototype.removeAllMarkers = function() {
            var marker;
            while (marker = this.markers[0]) {
                marker.destroy();
            }
        };

        /*
            Удаление всех оверлеев
         */
        cls.prototype.removeAllOverlays = function() {
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
        cls.prototype.geocode = function(address, success, error) {
            if (!this._geocoder) {
                this._geocoder = new google.maps.Geocoder();
            }

            var that = this;
            this._geocoder.geocode({
                address: address
            }, function(results, status) {
                if (status === google.maps.GeocoderStatus.OK) {
                    var native_point = results[0].geometry.location;
                    success.call(that, GMapPoint.fromNative(native_point));
                } else {
                    error.call(that, status, results);
                }
            });
        };
    });
    GMap.dataParamName = 'gmap';

})(jQuery);
