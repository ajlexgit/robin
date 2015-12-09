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
                    balloon: '<p>Hello</p>'
                });

                var marker2 = GMapMarker({
                    map: this,
                    position: GMapPoint(62.400471, -150.005608),
                    hint: 'second',
                    draggable: true,
                    balloon: '<p>Goodbay</p>'
                });

                var overlay = GMapOverlay({
                    map: this,
                    src: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/talkeetna.png',
                    coords: {
                        bottomleft: GMapPoint(62.281819, -150.287132),
                        topright: GMapPoint(62.400471, -150.005608)
                    }
                });

                this.center(GMapPoint(62.339889, -150.145683)).zoom(11);
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
                    return this;
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
                    return this;
                }

                this._map = value;
                this.native.setMap(this._map.native);
                this.trigger('attached');
                this._map.trigger('attach.marker', this);
            }

            return this;
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

            if (value && (typeof value != 'string')) {
                this.error('value should be a string');
                return this;
            }

            this.native.setIcon(value);
            return this;
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
                return this;
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
                return this;
            }

            this.native.setContent(value);
            return this;
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
            Открытие балуна
         */
        cls.prototype.open = function(marker_point) {
            if (marker_point instanceof GMapMarker) {
                this.native.open(this.map.native, marker_point.native);
            } else if (marker_point instanceof GMapPoint) {
                this.native.open(this.map.native);
                this.position(marker_point);
            } else {
                this.error('marker should be a GMapMarker or GMapPoint instance');
                return this;
            }

            this.opened = true;
            this.anchor = marker_point;
            this.trigger('opened');
            return this;
        };

        /*
            Закрытие балуна
         */
        cls.prototype.close = function() {
            this.native.close();
            this.opened = false;
            this.anchor = null;
            this.trigger('closed');
            return this;
        };
    });


    /*
        Класс наложения на карту Google
     */
    window.GMapOverlay = Class(EventedObject, function GMapOverlay(cls, superclass) {
        cls.prototype.init = function(options) {
            superclass.prototype.init.call(this);

            var opts = $.extend(true, {
                map: null,
                src: '',
                coords: {
                    topright: null,
                    bottomleft: null
                }
            }, options);

            // нативный объект
            var that = this;
            var native_class = new Function();
            native_class.prototype = new google.maps.OverlayView();
            native_class.prototype.onAdd = function() {
                that.onAdd.call(that);
            };
            native_class.prototype.draw = function() {
                that.draw.call(that);
            };
            native_class.prototype.onRemove = function() {
                that.onRemove.call(that);
            };
            this.native = new native_class();


            if (!opts.src) {
                return this.raise('src required');
            } else {
                this.src = opts.src;
            }

            if (!opts.coords) {
                return this.raise('coords required');
            } else if (opts.coords.bottomleft instanceof GMapPoint == false) {
                return this.raise('coords.bottomleft should be a GMapPoint instance');
            } else if (opts.coords.topright instanceof GMapPoint == false) {
                return this.raise('coords.topright should be a GMapPoint instance');
            } else {
                this.bounds = new google.maps.LatLngBounds(
                    opts.coords.bottomleft.native,
                    opts.coords.topright.native
                )
            }

            this.map(opts.map);
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            this.map(null);
            superclass.prototype.destroy.call(this);
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.prototype.onAdd = function() {
            this.container = document.createElement('div');
            this.container.style.position = 'absolute';

            var img = document.createElement('img');
            img.src = this.src;
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.position = 'absolute';
            this.container.appendChild(img);

            // Add the element to the "overlayLayer" pane.
            var panes = this.native.getPanes();
            panes.overlayLayer.appendChild(this.container);
        };

        /*
            Отрисовка оверлея
         */
        cls.prototype.draw = function() {
            // We use the south-west and north-east
            // coordinates of the overlay to peg it to the correct position and size.
            // To do this, we need to retrieve the projection from the overlay.
            var overlayProjection = this.native.getProjection();

            // Retrieve the south-west and north-east coordinates of this overlay
            // in LatLngs and convert them to pixel coordinates.
            // We'll use these coordinates to resize the div.
            var sw = overlayProjection.fromLatLngToDivPixel(this.bounds.getSouthWest());
            var ne = overlayProjection.fromLatLngToDivPixel(this.bounds.getNorthEast());

            // Resize the image's div to fit the indicated dimensions.
            this.container.style.left = sw.x + 'px';
            this.container.style.top = ne.y + 'px';
            this.container.style.width = (ne.x - sw.x) + 'px';
            this.container.style.height = (sw.y - ne.y) + 'px';
        };

        /*
            Вызывается при откреплении оверлея от карты
         */
        cls.prototype.onRemove = function() {
            this.container.parentNode.removeChild(this.container);
            this.container = null;
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
                this._map.trigger('detach.overlay', this);
                this.trigger('detached');
                this.native.setMap(null);
                this._map = null;
            }

            if (value !== null) {
                // подключение к новой карте
                if (value instanceof GMap == false) {
                    this.error('value should be a GMap instance');
                    return this;
                }

                this._map = value;
                this.native.setMap(this._map.native);
                this.trigger('attached');
                this._map.trigger('attach.overlay', this);
            }

            return this;
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

        var MAP_TYPES = [
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

            superclass.prototype.init.call(this);

            var opts = $.extend({
                center: null,
                mapType: 'roadmap',
                dblClickZoom: false,
                draggable: true,
                wheel: false,
                styles: [],
                zoom: 14,
                zoomControl: true
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

            // оверлеи на карте
            this.overlays = [];
            this.on('attach.overlay', function(e, overlay) {
                // добавление оверлея в массив
                that.overlays.push(overlay);
            }).on('detach.overlay', function(e, overlay) {
                // удаление оверлея из массива
                var index = that.overlays.indexOf(overlay);
                if (index >= 0) {
                    that.overlays.splice(index, 1);
                }
            });

            // инициализация
            cls.ready(function() {
                // нативный объект
                that.native = new google.maps.Map(that.$root.get(0), {
                    center: opts.center,
                    disableDoubleClickZoom: !opts.dblClickZoom,
                    disableDefaultUI: true,
                    zoomControl: opts.zoomControl
                });

                // Обработчик изменения размера экрана (например, для центрирования карты)
                google.maps.event.addDomListener(window, 'resize', $.rared(function() {
                    that.trigger('resize');
                }, 300));

                // создание балуна
                that.balloon = GMapBalloon(that, '');

                that.draggable(opts.draggable);
                that.mapType(opts.mapType);
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
                    return this;
                }

                this.native.setCenter(value.native);
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
        cls.prototype.panTo = function(center) {
            if (center instanceof GMapPoint == false) {
                this.error('value should be a GMapPoint instance');
                return this;
            }

            this.native.panTo(center);
            return this;
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
            if (MAP_TYPES.indexOf(value) < 0) {
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
