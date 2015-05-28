(function($) {

    /*
        Генерирует события перетаскивания.

        Параметры:
            preventDefaultDrag: true/false    - предотвратить Drag по-умолчанию
            speedInterval: 50                 - интервал обновления скорости мыши
            deceleration: [0-1]               - показатель плавности изменения скорости:
                                                0 - резкое изменение
                                                1 - отсутсвие изменения

            mouse:
                onStartDrag()                 - начало перетаскивания. Если вернет false,
                                                перетасквание будет отменено.
                onDrag(dX, dY)                - процесс перемещения
                onStopDrag(dX, dY)            - конец перемещения

            touch:
                onStartDrag()                 - начало перетаскивания. Если вернет false,
                                                перетасквание будет отменено.
                onDrag(dX, dY)                - процесс перемещения
                onStopDrag(dX, dY)            - конец перемещения
    */

    window.Drager = function($element, options) {
        var that = this;
        var settings = $.extend(true, {
            preventDefaultDrag: true,
            speedInterval: 100,
            deceleration: 0.33,

            mouse: {
                onStartDrag: $.noop,
                onDrag: $.noop,
                onStopDrag: $.noop
            },
            touch: {
                onStartDrag: $.noop,
                onDrag: $.noop,
                onStopDrag: $.noop
            }
        }, options);

        that.event = null;
        that.element = null;
        that.startPoint = {};

        that.speed = 0;
        that.speedPoint = {};
        that._lastPosX = -1;
        that._lastPosY = -1;
        that._distance = 0;
        that._lastTime = 0;
        that._speedTimer = null;

        that.getPoint = function() {
            return {
                pageX: that.event.pageX,
                pageY: that.event.pageY,
                clientX: that.event.clientX,
                clientY: that.event.clientY
            };
        };

        that.getDx = function(point) {
            point = point || that.startPoint;
            var clientDx = that.event.clientX - point.clientX;
            var pageDx = that.event.pageX - point.pageX;
            return (clientDx || pageDx) >=0 ? Math.max(clientDx, pageDx) : Math.min(clientDx, pageDx);
        };

        that.getDy = function(point) {
            point = point || that.startPoint;
            var clientDy = that.event.clientY - point.clientY;
            var pageDy = that.event.pageY - point.pageY;
            return (clientDy || pageDy) >= 0 ? Math.max(clientDy, pageDy) : Math.min(clientDy, pageDy);
        };

        that.updateDistance = function() {
            that._distance += Math.sqrt(
                Math.pow(that.getDx(that.speedPoint), 2) +
                Math.pow(that.getDy(that.speedPoint), 2)
            );
            that.speedPoint = that.getPoint();
        };

        that.updateSpeed = function() {
            var newSpeed = (1000 * that._distance) / (Date.now() - that._lastTime);
            that.speed = Math.round(
                settings.deceleration * that.speed +
                (1 - settings.deceleration) * newSpeed
            );
            that._distance = 0;
            that._lastTime = Date.now();
        };

        // === MOUSE ===
        if (settings.mouse) {
            // Блокируем дефолтовый Drag'n'Drop браузера
            if (settings.preventDefaultDrag) {
                $element.on('dragstart.drager', function() {
                    return false;
                });
            }

            $element.on('mousedown.drager', function(event) {
                that.event = event;
                that.element = this;
                that.startPoint = that.speedPoint = that.getPoint();

                if (settings.mouse.onStartDrag.call(that) === false) {
                    return;
                }

                that.speed = 0;
                that._distance = 0;
                that._lastTime = Date.now();
                that._speedTimer = setInterval(that.updateSpeed, settings.speedInterval);
            });

            $(document).on('mousemove.drager', function(event) {
                if (!that.element) return;

                that.event = event;
                that.updateDistance();
                settings.mouse.onDrag.call(that);
            }).on('mouseup.drager', function(event) {
                if (!that.element) return;

                that.event = event;
                that.element = null;
                clearInterval(that._speedTimer);
                that.updateSpeed();
                settings.mouse.onStopDrag.call(that);
            });
        }

        // === TOUCH ===
        if (settings.touch) {
            $element.on('touchstart.drager', function(event) {
                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                that.element = this;
                that.event = touchPoints[0];
                that.startPoint = that.speedPoint = that.getPoint();

                if (settings.touch.onStartDrag.call(that) === false) {
                    return;
                }

                that.speed = 0;
                that._distance = 0;
                that._lastTime = Date.now();
                that._speedTimer = setInterval(that.updateSpeed, settings.speedInterval);
            });

            $(document).on('touchmove.drager', function(event) {
                if (!that.element) return;

                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                that.event = touchPoints[0];
                that.updateDistance();
                settings.touch.onDrag.call(that);
            }).on('touchend.drager', function(event) {
                if (!that.element) return;

                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                that.element = null;
                that.event = touchPoints[0];
                clearInterval(that._speedTimer);
                that.updateSpeed();
                settings.touch.onStopDrag.call(that);
            });
        }
    };

})(jQuery);