(function($) {

    /*
        Генерирует события перетаскивания.

        Параметры:
            preventDefaultDrag: true/false    - предотвратить Drag по-умолчанию
            momentum: 500                     - величина инерции
            maxMomentumSpeed:3                - максимальная скорость инерционного движения

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

            mouse: true,
            touch: true,
            momentum: 200,
            maxMomentumSpeed: 3,

            onStartDrag: $.noop,
            onDrag: $.noop,
            onStopDrag: $.noop
        }, options);

        that._momentumPoints = [];
        that.drag = false;
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
                target: $element.get(0),
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
            } else {
                evt.dx = getDx(that.startPoint, evt.point);
                evt.dy = getDy(that.startPoint, evt.point);
                return evt;
            }
        };

        that.addMomentumPoint = function(evt) {
            var record =  {
                point: evt.point,
                timeStamp: evt.timeStamp
            };

            if (that._momentumPoints.length == 2) {
                that._momentumPoints.shift();
            }
            that._momentumPoints.push(record);
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
            $element.stop();

            var evt = that.getEvent(event, 'start');
            that.drag = true;
            that.startPoint = evt.point;

            that._momentumPoints = [];
            that.addMomentumPoint(evt);

            return settings.onStartDrag.call(that, evt);
        };

        var dragHandler = function(event) {
            if (!that.drag) return;

            var evt = that.getEvent(event, 'move');

            var lastMomentum = that._momentumPoints[that._momentumPoints.length - 1];
            if (evt.timeStamp - lastMomentum.timeStamp > 200) {
                that.addMomentumPoint(evt);
            }

            return settings.onDrag.call(that, evt);
        };

        var stopDragHandler = function(event) {
            if (!that.drag) return;
            that.drag = false;

            var evt = that.getEvent(event, 'stop');

            if (settings.momentum) {
                // Используем более старую точку, если последняя точка была
                // совсем недавно.
                var lastMomentum = that._momentumPoints[that._momentumPoints.length - 1];
                if (evt.timeStamp - lastMomentum.timeStamp < 100) {
                    if (that._momentumPoints.length == 2) {
                        lastMomentum = that._momentumPoints[0];
                    }
                }

                var dX = getDx(lastMomentum.point, evt.point);
                var dY = getDy(lastMomentum.point, evt.point);
                var duration = event.timeStamp - lastMomentum.timeStamp;
                var speedX = Math.abs(dX) / duration;
                var speedY = Math.abs(dY) / duration;

                // Ограничение скорости
                if (settings.maxMomentumSpeed) {
                    speedX = Math.min(speedX, settings.maxMomentumSpeed);
                    speedY = Math.min(speedY, settings.maxMomentumSpeed);
                }

                // Вычисление длительности и длины движения по инерции
                duration = Math.max(speedX, speedY) * settings.momentum;
                dX = speedX * duration * (dX >= 0 ? 1 : -1);
                dY = speedY * duration * (dX >= 0 ? 1 : -1);

                $element.css({
                    x: evt.dx,
                    y: evt.dy
                }).animate({
                    x: evt.dx + dX,
                    y: evt.dy + dY
                }, {
                    duration: duration,
                    easing: 'easeOutCubic',
                    step: function(now, fx) {
                        if (fx.prop == 'x') {
                            evt.dx = Math.round(now);
                        } else {
                            evt.dy = Math.round(now);
                        }
                        evt.timeStamp = Date.now();
                        settings.onDrag.call(that, evt);
                    }
                })
            }

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