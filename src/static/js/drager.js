(function($) {

    /*
        Генерирует события перетаскивания.

        Параметры:
            preventDefaultDrag: true/false    - предотвратить Drag по-умолчанию
            deceleration: 0.002               - показатель замедления:

            onStartDrag(event)                - нажатие на элемент
            onDrag(event)                     - процесс перемещения
            onStopDrag(event)                 - отпускание элемента
    */

    var getDx = function(fromPoint, toPoint) {
        var clientDx = toPoint.clientX - fromPoint.clientX;
        var pageDx = toPoint.pageX - fromPoint.pageX;
        return (clientDx || pageDx) >= 0 ? Math.max(clientDx, pageDx) : Math.min(clientDx, pageDx);
    };

    var getDy = function (fromPoint, toPoint) {
        var clientDy = toPoint.clientY - fromPoint.clientY;
        var pageDy = toPoint.pageY - fromPoint.pageY;
        return (clientDy || pageDy) >= 0 ? Math.max(clientDy, pageDy) : Math.min(clientDy, pageDy);
    };

    window.Drager = function($element, options) {
        var that = this;
        var settings = $.extend(true, {
            preventDefault: true,
            deceleration: 0.002,

            mouse: true,
            touch: true,

            onStartDrag: $.noop,
            onDrag: $.noop,
            onStopDrag: $.noop
        }, options);

        that.element = null;
        that._momentum = {};

        that.getEvent = function(event, type) {
            var pointEvent;
            if (event.type.substr(0, 5) == 'mouse') {
                pointEvent = event;
            } else {
                var orig = event.originalEvent;
                if (typeof orig.changedTouches != 'undefined') {
                    pointEvent = orig.changedTouches[0];
                } else {
                    pointEvent = orig;
                }
            }

            var evt = {
                type: type,
                origEvent: event,
                timeStamp: event.timeStamp,
                point: {
                    pageX: pointEvent.pageX,
                    pageY: pointEvent.pageY,
                    clientX: pointEvent.clientX,
                    clientY: pointEvent.clientY
                },
                target: that.element || event.target
            };

            if (type == 'start') {
                evt.dx = 0;
                evt.dy = 0;
                return evt;
            } else if (type == 'move') {
                evt.dx = getDx(that.startPoint, evt.point);
                evt.dy = getDy(that.startPoint, evt.point);
                return evt;
            } else if (type == 'stop') {
                evt.dx = getDx(that.startPoint, evt.point);
                evt.dy = getDy(that.startPoint, evt.point);
                evt.momentum = that.getMomentum(event, evt.point);
                return evt;
            }
        };

        that.getMomentum = function(event, toPoint) {
            var duration = event.timeStamp - that._momentum.time;
            var dX = getDx(that._momentum.point, toPoint);
            var dY = getDy(that._momentum.point, toPoint);
            var speedX = Math.abs(dX) / duration;
            var speedY = Math.abs(dY) / duration;
            return {
                dX: Math.round((speedX * speedX) / (2 * settings.deceleration) * (dX >= 0 ? 1 : -1)),
                dY: Math.round((speedY * speedY) / (2 * settings.deceleration) * (dY >= 0 ? 1 : -1)),
                duration: Math.round(Math.max(speedX, speedY) / settings.deceleration)
            };
        };

        that.isMultiTouch = function(event) {
            var orig = event.originalEvent;
            var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
            return touchPoints.length > 1;
        };

        // === MOUSE ===
        if (settings.mouse) {
            // Блокируем дефолтовый Drag'n'Drop браузера
            if (settings.preventDefault) {
                $element.on('dragstart.drager', function() {
                    return false;
                });
            }

            $element.on('mousedown.drager', function(event) {
                var evt = that.getEvent(event, 'start');

                that.element = this;
                that.startPoint = evt.point;

                that._momentum.point = evt.point;
                that._momentum.time = evt.timeStamp;

                return settings.onStartDrag.call(that, evt);
            });

            $(document).on('mousemove.drager', function(event) {
                if (!that.element) return;

                var evt = that.getEvent(event, 'move');

                if (evt.timeStamp - that._momentum.time > 200) {
                    that._momentum.point = evt.point;
                    that._momentum.time = evt.timeStamp;
                }

                return settings.onDrag.call(that, evt);
            }).on('mouseup.drager', function(event) {
                if (!that.element) return;

                var evt = that.getEvent(event, 'stop');

                that.element = null;
                return settings.onStopDrag.call(that, evt);
            });
        }

        // === TOUCH ===
        if (settings.touch) {
            $element.on('touchstart.drager', function(event) {
                if (that.isMultiTouch(event)) return;

                var evt = that.getEvent(event, 'start');

                that.element = this;
                that.startPoint = evt.point;

                that._momentum.point = evt.point;
                that._momentum.time = evt.timeStamp;

                return settings.onStartDrag.call(that, evt);
            });

            $(document).on('touchmove.drager', function(event) {
                if (!that.element) return;
                if (that.isMultiTouch(event)) return;

                var evt = that.getEvent(event, 'move');

                if (evt.timeStamp - that._momentum.time > 200) {
                    that._momentum.point = evt.point;
                    that._momentum.time = evt.timeStamp;
                }

                return settings.onDrag.call(that, evt);
            }).on('touchend.drager', function(event) {
                if (!that.element) return;
                if (that.isMultiTouch(event)) return;

                var evt = that.getEvent(event, 'stop');

                that.element = null;
                return settings.onStopDrag.call(that, evt);
            });
        }
    };

})(jQuery);