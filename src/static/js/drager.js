(function($) {

    /*
        Генерирует события перетаскивания.

        Параметры:
            preventDefaultDrag: true/false    - предотвратить Drag по-умолчанию
            deceleration: [0-1]               - показатель замедления:

            onStartDrag(event)                - нажатие на элемент
            onDrag(event)                     - процесс перемещения
            onStopDrag(event)                 - отпускание элемента
    */

    var getTime = Date.now || function() {
            return new Date().getTime();
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
            var evt = {
                type: type,
                origEvent: event,
                timeStamp: event.timeStamp,
                point: that.getPoint(event)
            };

            if (type == 'start') {
                evt.dx = 0;
                evt.dy = 0;
                return evt;
            } else if (type == 'move') {
                evt.dx = that.getDx(event);
                evt.dy = that.getDy(event);
                evt.startPoint = that.startPoint;
                return evt;
            } else if (type == 'stop') {
                evt.dx = that.getDx(event);
                evt.dy = that.getDy(event);
                evt.momentum = that.getMomentum(event);
                evt.startPoint = that.startPoint;
                return evt;
            }
        };

        that.getPoint = function(event) {
            return {
                pageX: event.pageX,
                pageY: event.pageY,
                clientX: event.clientX,
                clientY: event.clientY
            };
        };

        that.getDx = function(event, point) {
            point = point || that.startPoint;
            var clientDx = event.clientX - point.clientX;
            var pageDx = event.pageX - point.pageX;
            return (clientDx || pageDx) >=0 ? Math.max(clientDx, pageDx) : Math.min(clientDx, pageDx);
        };

        that.getDy = function(event, point) {
            point = point || that.startPoint;
            var clientDy = event.clientY - point.clientY;
            var pageDy = event.pageY - point.pageY;
            return (clientDy || pageDy) >= 0 ? Math.max(clientDy, pageDy) : Math.min(clientDy, pageDy);
        };

        that.getMomentum = function(event) {
            var duration = getTime() - that._momentum.time;
            var dX = that.getDx(event, that._momentum.point);
            var dY = that.getDy(event, that._momentum.point);
            var speedX = Math.abs(dX) / duration;
            var speedY = Math.abs(dY) / duration;
            return {
                dX: (speedX * speedX) / (2 * settings.deceleration) * (dX >= 0 ? 1 : -1),
                dY: (speedY * speedY) / (2 * settings.deceleration) * (dY >= 0 ? 1 : -1),
                duration: Math.max(speedX, speedY) / settings.deceleration
            };
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
                var result = settings.onStopDrag.call(that, evt);
                that.element = null;
                return result;
            });
        }

        // === TOUCH ===
        if (settings.touch) {
            $element.on('touchstart.drager', function(event) {
                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                var evt = that.getEvent(touchPoints[0], 'start');

                that.element = this;
                that.startPoint = evt.point;

                that._momentum.point = evt.point;
                that._momentum.time = evt.timeStamp;

                return settings.onStartDrag.call(that, evt);
            });

            $(document).on('touchmove.drager', function(event) {
                if (!that.element) return;

                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                var evt = that.getEvent(touchPoints[0], 'move');

                if (evt.timeStamp - that._momentum.time > 200) {
                    that._momentum.point = evt.point;
                    that._momentum.time = evt.timeStamp;
                }

                return settings.onDrag.call(that, evt);
            }).on('touchend.drager', function(event) {
                if (!that.element) return;

                var orig = event.originalEvent;
                var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
                if (touchPoints.length > 1) return;

                var evt = that.getEvent(touchPoints[0], 'stop');
                var result = settings.onStopDrag.call(that, evt);
                that.element = null;
                return result;
            });
        }
    };

})(jQuery);