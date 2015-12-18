(function($) {


    /*
        Базовый класс всплывающего окна.

        Задает положение на карте, DOM-разметку и содержимое.

        Генерируемые события:
            added   - DOM добавлен на карту
            open    - после открытия окна
            close   - после закрытия окна

     */

    // события, не всплывающие на окне
    var MOUSE_EVENTS = [
        'mousedown', 'mousemove', 'mouseover', 'mouseout', 'mouseup',
        'mousewheel', 'DOMMouseScroll', 'touchstart', 'touchend', 'touchmove',
        'dblclick', 'contextmenu', 'click'
    ];

    window.GMapBalloonBase = Class(GMapOverlayBase, function GMapBalloonBase(cls, superclass) {
        cls.prototype.layer = 'floatPane';

        cls.prototype.NATIVE_EVENTS = [
            'domready',
            'closeclick',
            'content_changed',
            'position_changed'
        ];

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                content: '',
                position: null
            });
        };

        /*
            Инициализация
         */
        cls.prototype.onInit = function() {
            if (this.opts.position) {
                if (this.opts.position instanceof GMapPoint == false) {
                    return this.raise('position should be a GMapPoint instance');
                }
            }

            superclass.prototype.onInit.call(this);

            // точка
            this._position = this.opts.position;

            // состояние
            this._opened = false;

            this._buildDOM();

            this._content = null;
            this.content(this.opts.content);
        };


        /*
            Построение DOM
         */
        cls.prototype._buildDOM = function() {
            this.$container = $('<div>').addClass('gmap-balloon').hide();
            this.$content = $('<div>').addClass('gmap-balloon-content');
            this.$closeBtn = $('<div>').addClass('gmap-balloon-close');

            this.$container.append(this.$closeBtn, this.$content);
        };

        /*
            Рассчет размеров окна
         */
        cls.prototype.updateSize = function() {
            this.$container.css({
                width: '',
                height: ''
            });

            this._width = this.$container.outerWidth();
            this._height = this.$container.outerHeight();

            this.$container.css({
                width: this._width
            });
        };


        /*
            Позиционирование окна
         */
        cls.prototype.updatePosition = function() {
            if (!this._opened) {
                return
            }

            if (!this._position) {
                this.error('position required');
                return
            }

            var projection = this.native.getProjection();
            var pos = projection.fromLatLngToDivPixel(this.position().native);
            this._updatePosition(pos);
        };


        /*
            Позиционирование окна
         */
        cls.prototype._updatePosition = function(pos) {
            this.$container.css({
                left: pos.x - this._width / 2,
                top: pos.y - this._height
            });
        };

        /*
            Вызывается при добавлении оверлея на карту
         */
        cls.prototype.onAdd = function() {
            superclass.prototype.onAdd.call(this);

            // закрытие окна при клике на крестик
            var that = this;
            this._closeListener = google.maps.event.addDomListener(this.$closeBtn.get(0), 'click', function() {
                that.close();
                google.maps.event.trigger(that.native, 'closeclick');
            });

            // Запрещаем всплытие некоторых событий на окне, чтобы можно было выделять текст
            this._listeners = [];
            for (var i = 0, event; event = MOUSE_EVENTS[i]; i++) {
                var handler = google.maps.event.addDomListener(this.$container.get(0), event, function(e) {
                    e.cancelBubble = true;
                    if (e.stopPropagation) {
                        e.stopPropagation();
                    }
                });
                this._listeners.push(handler);
            }

            google.maps.event.trigger(this.native, 'domready');
            this.trigger('added');
        };

        /*
            Отрисовка оверлея
         */
        cls.prototype.draw = function() {
            this.updatePosition();
        };

        /*
            Вызывается при откреплении оверлея от карты
         */
        cls.prototype.onRemove = function() {
            // удаление обработчиков мыши на окне
            for (var i = 0, listener; listener = this._listeners[i]; i++) {
                google.maps.event.removeListener(listener);
            }

            google.maps.event.removeListener(this._closeListener);
            superclass.prototype.onRemove.call(this);
        };

        /*
            Событие загрузки картинки
         */
        cls.prototype.onImageLoaded = function() {
            this.updateSize();
            this.updatePosition()
        };

        /*
            Показ окна
         */
        cls.prototype.open = function() {
            if (this._opened) {
                return false
            } else {
                this._opened = true;
            }

            var that = this;
            var args = Array.prototype.concat(arguments);
            setTimeout(function() {
                that.updatePosition();
                that._open.apply(that, args);
            }, 0);
        };

        /*
            Анимация показа окна
         */
        cls.prototype._open = function() {
            var that = this;
            this.$container.fadeIn({
                duration: 100,
                complete: function() {
                    that.trigger('open');
                }
            });
        };

        /*
            Закрытие окна
         */
        cls.prototype.close = function() {
            if (!this._opened) {
                return false
            } else {
                this._opened = false;
            }

            this._close.apply(this, arguments);
        };

        /*
            Анимация закрытия окна
         */
        cls.prototype._close = function() {
            var that = this;
            this.$container.fadeOut({
                duration: 100,
                complete: function() {
                    that.trigger('close');
                }
            });
        };

        /*
            Получение / установка положения
         */
        cls.prototype.position = function(value) {
            if (value === undefined) {
                // получение положения
                return this._position;
            }

            if (value) {
                if (value instanceof GMapPoint == false) {
                    this.error('value should be a GMapPoint instance');
                    return this;
                }

                this._position = value;
                this.updatePosition();
                google.maps.event.trigger(this.native, 'position_changed');
            }

            return this;
        };

        /*
            Получение / установка содержимого всплывающего окна
         */
        cls.prototype.content = function(value) {
            if (value === undefined) {
                // получение содержимого
                return this._content;
            }

            if (value && (typeof value != 'string')) {
                this.error('value should be a string');
                return this;
            }

            if (this._content === null) {
                // установка контента при инициализации
                this._content = value;
                this.$content.html(this._content);
            } else {
                // установка контента после инициализации
                this._content = value;
                this.$content.html(this._content);

                this.updateSize();
                this.updatePosition();
                google.maps.event.trigger(this.native, 'content_changed');
            }

            // перерисовка при загрузке картинок
            var that = this;
            this.$container.find('img').on('load', function() {
                that.onImageLoaded();
            });

            return this;
        };
    });


    /*
        Всплывающее окно, привязанное к маркеру
     */
    window.GMapBalloon = Class(GMapBalloonBase, function GMapBalloon(cls, superclass) {
        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                autoPan: true
            });
        };

        /*
            Инициализация
         */
        cls.prototype.onInit = function() {
            superclass.prototype.onInit.call(this);

            // привязка к маркеру
            this._anchor = null;
        };

        /*
            Построение DOM
         */
        cls.prototype._buildDOM = function() {
            superclass.prototype._buildDOM.call(this);

            this.$arrow = $('<div>').addClass('gmap-balloon-arrow');
            this.$container.append(this.$arrow);
        };

        /*
            Событие загрузки картинки
         */
        cls.prototype.onImageLoaded = function() {
            if (this.opts.autoPan) {
                this.panToView()
            }

            this.updateSize();
            this.updatePosition();
        };

        /*
            Показ окна
         */
        cls.prototype.open = function(marker) {
            if (!marker) {
                this.error('marker required');
                return
            } else if (marker instanceof GMapMarker == false) {
                this.error('marker should be a GMapMarker instance');
                return
            }

            // отвязывание события со старого маркера
            if (this._anchor) {
                this._anchor.off('.balloon');
            }

            this._anchor = marker;
            this.position(this._anchor.position());

            var that = this;
            this._anchor.one('detached.balloon', function() {
                // закрываем окно при удалении маркера с карты
                that._anchor = null;
                that.close();
            });
            this._anchor.on('dragend.balloon', function() {
                // меняем положение окна при перемещении маркера
                that.position(this.position());
            });

            superclass.prototype.open.call(this);
        };

        /*
            Анимация показа окна
         */
        cls.prototype._open = function() {
            if (this.opts.autoPan) {
                this.panToView()
            }

            superclass.prototype._open.call(this);
        };

        /*
            Позиционирование окна
         */
        cls.prototype._updatePosition = function(pos) {
            this.$container.css({
                left: pos.x - this._width / 2,
                top: pos.y - this._height - this._getAnchorHeight()
            });
        };

        /*
            Перемещение карты к окну
         */
        cls.prototype.panToView = function() {
            if (!this._opened) {
                return
            }

            this.updateSize();

            var map = this.map();
            var mapDiv = map.native.getDiv();
            var mapHeight = mapDiv.offsetHeight;

            var latLng = this.position().native;
            var projection = this.native.getProjection();

            var centerPos = projection.fromLatLngToContainerPixel(map.center().native);
            var coords = projection.fromLatLngToContainerPixel(latLng);

//            // Find out how much space at the top is free
//            var spaceTop = centerPos.y - this._height - this._getAnchorHeight();
//
//            // Fine out how much space at the bottom is free
//            var spaceBottom = mapHeight - centerPos.y;

            var totalHeight = this._height + this._getAnchorHeight();
            if (totalHeight < mapHeight) {
                coords.y -= totalHeight / 2;
            }

            latLng = projection.fromContainerPixelToLatLng(coords);

            map.panTo(GMapPoint.fromNative(latLng));
        };

        /*
            Получение высоты маркера
         */
        cls.prototype._getAnchorHeight = function() {
            if (!this._anchor) {
                return
            }

            var icon = this._anchor.icon();
            if (icon && icon.size) {
                return icon.size.height;
            } else {
                return 40;
            }
        }
    });

})(jQuery);
