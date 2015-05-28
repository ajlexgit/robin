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

    var getTime = Date.now || function() {
            return new Date().getTime();
        };

    window.Drager = function($element, options) {
        var that = this;
        var settings = $.extend(true, {
            preventDefaultDrag: true,
            speedInterval: 100,
            deceleration: 0.002,

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

                that.startTime = getTime();
            });

            $(document).on('mousemove.drager', function(event) {
                if (!that.element) return;

                that.event = event;

                var timestamp = getTime();
                if (timestamp - that.startTime > 200) {
                    that.startTime = timestamp;
                    that.speedPoint = that.getPoint();
                }

                settings.mouse.onDrag.call(that);
            }).on('mouseup.drager', function(event) {
                if (!that.element) return;

                that.event = event;

                var duration = getTime() - that.startTime;
                var dX = that.getDx(that.speedPoint);
                var dY = that.getDy(that.speedPoint);
                var speedX = Math.abs(dX) / duration;
                var speedY = Math.abs(dY) / duration;
                var momentum = {
                    dX: (speedX * speedX) / (2 * settings.deceleration) * (dX >= 0 ? 1 : -1),
                    dY: (speedY * speedY) / (2 * settings.deceleration) * (dY >= 0 ? 1 : -1),
                    duration: Math.max(speedX, speedY) / settings.deceleration
                };

                settings.mouse.onStopDrag.call(that, momentum);

                that.element = null;
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

                that.startTime = getTime();
            });

            $(document).on('touchmove.drager', function(event) {
                if (!that.element) return;

                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                that.event = touchPoints[0];

                var timestamp = getTime();
                if (timestamp - that.startTime > 200) {
                    that.startTime = timestamp;
                    that.speedPoint = that.getPoint();
                }

                settings.touch.onDrag.call(that);
            }).on('touchend.drager', function(event) {
                if (!that.element) return;

                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                that.event = touchPoints[0];

                var duration = getTime() - that.startTime;
                var dX = that.getDx(that.speedPoint);
                var dY = that.getDy(that.speedPoint);
                var speedX = Math.abs(dX) / duration;
                var speedY = Math.abs(dY) / duration;
                var momentum = {
                    dX: (speedX * speedX) / (2 * settings.deceleration) * (dX >= 0 ? 1 : -1),
                    dY: (speedY * speedY) / (2 * settings.deceleration) * (dY >= 0 ? 1 : -1),
                    duration: Math.max(speedX, speedY) / settings.deceleration
                };

                settings.mouse.onStopDrag.call(that, momentum);

                that.element = null;
            });
        }
    };

})(jQuery);