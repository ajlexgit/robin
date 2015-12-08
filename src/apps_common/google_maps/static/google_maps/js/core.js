(function($) {

    /*
        Карта Google.

        Требует:
            jquery.utils.js


        Рекомендуется работать с картой в обработчике события GMap.ready().

        var gmap = GMap('#gmap', {
            center: GMapPoint(53.510171, 49.418785),
            zoom: 2
        }).on('ready', function() {
            var marker1 = GMapMarker({
                map: this,
                position: GMapPoint(53.510171, 49.418785),
                hint: 'First',
                balloon: '<p>Hello</p>'
            });

            var marker2 = GMapMarker({
                map: this,
                position: GMapPoint(53.525000, 49.435000),
                hint: 'second',
                draggable: true,
                balloon: '<p>Goodbay</p>'
            });

            this.center(this.markers[0].position());
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
            this.native = new google.maps.LatLng(this.lat, this.lng);
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
    window.GMapMarker = Class(EventedObject, function GMapMarker(cls, superclass) {
        var NATIVE_EVENTS = [
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

        cls.prototype.init = function(options) {
            superclass.prototype.init.call(this);

            var opts = $.extend({
                map: null,
                position: null,
                icon: '',
                hint: '',
                balloon: '',
                draggable: false
            }, options);

            // нативный объект
            this.native = new google.maps.Marker();

            // массив событий, которые повешены на нативный маркер
            this.native_events = [];

            this.map(opts.map);
            this.position(opts.position);
            this.icon(opts.icon);
            this.hint(opts.hint);
            this.balloon(opts.balloon);
            this.draggable(opts.draggable);
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            this.map(null);

            this.native_events = [];
            google.maps.event.clearInstanceListeners(this.native);

            superclass.prototype.destroy.call(this);
        };

        /*
            Отлов событий
         */
        cls.prototype.on = function(name, handler) {
            var evt_info = this._formatEventName(name);
            var evt_name = evt_info.name;
            if (evt_name && (this.native_events.indexOf(evt_name) < 0) && (NATIVE_EVENTS.indexOf(evt_name) >= 0)) {
                // вешаем обработчик на нативный маркер при первом обращении
                var that = this;
                this.native_events.push(evt_name);
                this.native.addListener(evt_name, function() {
                    that.trigger(evt_name);
                });
            }

            return superclass.prototype.on.call(this, name, handler);
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
                    return
                }

                // отключение от текущей карты
                if (this._map.balloon.anchor == this) {
                    this._map.balloon.close();
                }

                this._map.trigger('detach.marker', this);
                this.trigger('detached');
                this.native.setMap(null);
                this._map = null;
            }

            if (value !== null) {
                // подключение к новой карте
                if (value instanceof GMap == false) {
                    this.error('value should be a GMap instance');
                    return false;
                }

                this._map = value;
                this.native.setMap(this._map.native);
                this.trigger('attached');
                this._map.trigger('attach.marker', this);
            }
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
                    return false;
                }

                this.native.setPosition(value.native);
            }
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
                return false;
            }

            this.native.setTitle(value);
        };

        /*
            Получение / установка иконки
         */
        cls.prototype.icon = function(value) {
            if (value === undefined) {
                // получение иконки
                return this.native.getIcon();
            }

            if (value && (typeof value != 'string')) {
                this.error('value should be a string');
                return false;
            }

            this.native.setIcon(value);
        };

        /*
            Получение / установка HTML всплывающего окна
         */
        cls.prototype.balloon = function(value) {
            if (value === undefined) {
                // получение HTML
                return this._balloon;
            }

            if (value && (typeof value != 'string')) {
                this.error('value should be a string');
                return false;
            }

            this._balloon = value;

            if (value) {
                var that = this;
                this.on('click.balloon', function() {
                    var map = that.map();
                    if (map) {
                        map.balloon.content(that._balloon);
                        map.balloon.open(that);
                    }
                });
            } else {
                this.off('click.balloon');
            }
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
        };
    });


    /*
        Класс для всплывающего окна карты
     */
    window.GMapBalloon = Class(EventedObject, function GMapBalloon(cls, superclass) {
        cls.prototype.init = function(map, content) {
            superclass.prototype.init.call(this);

            if (typeof content != 'string') {
                return this.raise('content should be a string');
            }

            if (map instanceof GMap == false) {
                return this.raise('map should be a GMap instance');
            } else {
                this.map = map;
            }

            // нативный объект
            this.native = new google.maps.InfoWindow({
                content: content
            });

            this.opened = false;
            this.anchor = null;
        };

        /*
            Получение / установка содержимого всплывающего окна
         */
        cls.prototype.content = function(value) {
            if (value === undefined) {
                // получение содержимого
                return this.native.getContent();
            }

            if (value && (typeof value != 'string')) {
                this.error('value should be a string');
                return false;
            }

            this.native.setContent(value);
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
                    return false;
                }

                this.native.setPosition(value.native);
            }
        };

        /*
            Открытие балуна
         */
        cls.prototype.open = function(marker) {
            if (marker instanceof GMapMarker == false) {
                this.error('marker should be a GMapMarker instance');
                return false;
            }

            this.native.open(this.map.native, marker.native);
            this.opened = true;
            this.anchor = marker;
            this.trigger('opened');
        };

        /*
            Закрытие балуна
         */
        cls.prototype.close = function() {
            this.native.close();
            this.opened = false;
            this.anchor = null;
            this.trigger('closed');
        };
    });


    /*
        Класс карты Google
     */
    window.GMap = Class(EventedObject, function GMap(cls, superclass) {
        var NATIVE_EVENTS = [
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

            superclass.prototype.init.call(this);

            var opts = $.extend({
                center: null,
                wheel: false,
                styles: [],
                zoom: 14
            }, options);

            // массив событий, которые повешены на нативный маркер
            this.native_events = [];

            // маркеры на карте
            var that = this;
            this.markers = [];
            this.on('attach.marker', function(e, marker) {
                // добавление маркера в массив
                that.markers.push(marker);
            }).on('detach.marker', function(e, marker) {
                // удаление маркера из массива
                var index = that.markers.indexOf(marker);
                if (index >= 0) {
                    that.markers.splice(index, 1);
                }
            });

            // инициализация
            cls.ready(function() {
                // нативный объект
                that.native = new google.maps.Map(that.$root.get(0), {
                    center: GMapPoint(53.510171, 49.418785).native,
                    disableDoubleClickZoom: true,
                    disableDefaultUI: true,
                    zoomControl: true
                });

                // Обработчик изменения размера экрана (например, для центрирования карты)
                google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                    that.trigger('resize');
                }, 300));

                // создание балуна
                that.balloon = GMapBalloon(that, '');

                that.center(opts.center);
                that.wheel(opts.wheel);
                that.styles(opts.styles);
                that.zoom(opts.zoom);

                setTimeout(function() {
                    that.trigger('ready');
                }, 0);
            });

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Отлов событий
         */
        cls.prototype.on = function(name, handler) {
            var evt_info = this._formatEventName(name);
            var evt_name = evt_info.name;
            if (evt_name && (this.native_events.indexOf(evt_name) < 0) && (NATIVE_EVENTS.indexOf(evt_name) >= 0)) {
                // вешаем обработчик на нативную карту при первом обращении
                var that = this;
                this.native_events.push(evt_name);
                this.native.addListener(evt_name, function() {
                    that.trigger(evt_name);
                });
            }

            return superclass.prototype.on.call(this, name, handler);
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
                if (value instanceof GMapPoint == false) {
                    this.error('value should be a GMapPoint instance');
                    return false;
                }

                this.native.setCenter(value.native);
            }
        };

        /*
            Плавное перемещение к точке
         */
        cls.prototype.panTo = function(center) {
            if (center instanceof GMapPoint == false) {
                this.error('value should be a GMapPoint instance');
                return false;
            }

            this.native.panTo(center);
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
                return false;
            }

            this.native.set('styles', value);
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
                return false;
            }

            this.native.setZoom(value);
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
