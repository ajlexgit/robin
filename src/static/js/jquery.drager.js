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

    var getDy = function(fromPoint, toPoint) {
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

        that._element = null;
        that._momentum = {};
        that.startPoint = null;

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
                target: that._element,
                timeStamp: event.timeStamp,
                point: {
                    pageX: pointEvent.pageX,
                    pageY: pointEvent.pageY,
                    clientX: pointEvent.clientX,
                    clientY: pointEvent.clientY
                }
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

        // ================
        // === Handlers ===
        // ================
        var startDragHandler = function(event) {
            that._element = this;
            var evt = that.getEvent(event, 'start');

            that.startPoint = evt.point;
            that._momentum.point = evt.point;
            that._momentum.time = evt.timeStamp;
            return settings.onStartDrag.call(that, evt);
        };

        var dragHandler = function(event) {
            if (!that._element) return;

            var evt = that.getEvent(event, 'move');
            if (evt.timeStamp - that._momentum.time > 200) {
                that._momentum.point = evt.point;
                that._momentum.time = evt.timeStamp;
            }

            return settings.onDrag.call(that, evt);
        };

        var stopDragHandler = function(event) {
            if (!that._element) return;

            var evt = that.getEvent(event, 'stop');
            that._element = null;
            return settings.onStopDrag.call(that, evt);
        };

        // ====================
        // === Mouse Events ===
        // ====================
        if (settings.mouse) {
            // Блокируем дефолтовый Drag'n'Drop браузера
            if (settings.preventDefault) {
                $element.on('dragstart.drager', function() {
                    return false;
                });
            }

            $element.on('mousedown.drager', startDragHandler);
            $(document).on('mousemove.drager', dragHandler);
            $(document).on('mouseup.drager', stopDragHandler);
        }

        // ====================
        // === Touch Events ===
        // ====================
        if (settings.touch) {
            $element.on('touchstart.drager', function(event) {
                if (that.isMultiTouch(event)) return;
                return startDragHandler.call(this, event);
            });
            $(document).on('touchmove.drager', function(event) {
                if (that.isMultiTouch(event)) return;
                return dragHandler.call(this, event);
            }).on('touchend.drager', function(event) {
                if (that.isMultiTouch(event)) return;
                return stopDragHandler.call(this, event);
            });
        }
    };

})(jQuery);