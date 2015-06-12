(function($) {

    /*
        Генерирует события перетаскивания. Реального перемещения не делает.
        Это только интерфейс для реализации разных штук.
        Есть настройки для реализации продолжения движения по инерции
        при отпускании кнопки мыши.

        Требует:
            jquery.animation.js

        Параметры:
            preventDefaultDrag: true/false    - предотвратить событие drag по-умолчанию
            mouse: true                       - разрешить перетаскивание мышью
            touch: true                       - разрешить перетаскивание тачпадом
            ignoreDistance: 10                - игнорировать краткие движения
            momentumWeight: 500               - "вес" инерции (0 - нет инерции)
            momentumEasing: 'easeOutCubic'    - функция сглаживания иенрционного движения

            onMouseDown(event)                - нажатие мышью или тачпадом
            onStartDrag(event)                - начало перемещения
            onDrag(event)                     - процесс перемещения
            onStopDrag(event)                 - конец перемещения
            onMouseUp(event)                  - отпускание элемента

        Примеры:
            var drager = $.drager($element, {
                onMouseDown: function(evt) {
                    ...

                    // Prevent default event (mousedown, touchstart)
                    return false
                },
                onStartDrag: function(evt) {
                    ...
                },
                onDrag: function(evt) {
                    var $element = $(evt.target);

                    console.log('Diff X =', Math.abs(evt.dx));
                    console.log('Diff Y =', Math.abs(evt.dy));
                    console.log('startPoint =', evt.startPoint);
                    console.log('current point =', evt.point);

                    // Prevent default event (mousemove, touchmove)
                    return false
                },
                onMouseUp: function(evt) {
                    // Prevent momentum
                    evt.momentum = null;

                    // Override momentum
                    evt.momentum.setMomentumSpeed(undefined, 1);    // меняет duration
                    evt.momentum.setMomentumWeight(600);            // меняет duration
                    evt.momentum.setMomentumEndPoint(200, 400);     // меняет duration
                    evt.momentum.setMomentumDuration(2000);
                    evt.momentum.setMomentumEasing('linear');

                    // Prevent default event (mouseup, touchend);
                    return false
                },
                onStopDrag: function(evt) {
                    // тоже самое, что в onMouseUp
                },
            });
    */

    var getDx = function (fromPoint, toPoint) {
        var clientDx = toPoint.clientX - fromPoint.clientX;
        var pageDx = toPoint.pageX - fromPoint.pageX;
        return (clientDx || pageDx) >= 0 ? Math.max(clientDx, pageDx) : Math.min(clientDx, pageDx);
    };

    var getDy = function (fromPoint, toPoint) {
        var clientDy = toPoint.clientY - fromPoint.clientY;
        var pageDy = toPoint.pageY - fromPoint.pageY;
        return (clientDy || pageDy) >= 0 ? Math.max(clientDy, pageDy) : Math.min(clientDy, pageDy);
    };

    var DragerEvent = function (properties) {
        $.extend(true, this, properties);

        this.initMomentum = function (evt, lastMomentumRecord) {
            var dx = getDx(lastMomentumRecord.point, evt.point);
            var dy = getDy(lastMomentumRecord.point, evt.point);
            var duration = evt.origEvent.timeStamp - lastMomentumRecord.timeStamp;

            this.setMomentumSpeed(dx / duration, dy / duration);
        };

        this.setMomentumSpeed = function (speedX, speedY) {
            if (typeof speedX != 'undefined') {
                this.momentum.speedX = speedX;
            }
            if (typeof speedY != 'undefined') {
                this.momentum.speedY = speedY;
            }

            var speed = Math.max(Math.abs(this.momentum.speedX), Math.abs(this.momentum.speedY));
            this.setMomentumDuration(speed * this.momentum.weight);
        };

        this.setMomentumWeight = function (weight) {
            this.momentum.weight = weight;

            var speed = Math.max(Math.abs(this.momentum.speedX), Math.abs(this.momentum.speedY));
            this.setMomentumDuration(speed * this.momentum.weight);
        };

        this.setMomentumEndPoint = function (endX, endY) {
            var dx = endX - this.momentum.startX;
            var dy = endY - this.momentum.startY;
            var tx = this.momentum.speedX ? Math.abs(dx / this.momentum.speedX) : 0;
            var ty = this.momentum.speedY ? Math.abs(dy / this.momentum.speedY) : 0;

            this.momentum.duration = Math.max(tx, ty) || 0;
            this.momentum.endX = endX;
            this.momentum.endY = endY;
        };

        this.setMomentumDuration = function (duration) {
            this.momentum.duration = Math.abs(duration) || 0;
            this.momentum.endX = this.momentum.startX + this.momentum.speedX * this.momentum.duration;
            this.momentum.endY = this.momentum.startY + this.momentum.speedY * this.momentum.duration;
        };

        this.setMomentumEasing = function (easing) {
            this.momentum.easing = easing;
        };
    };

    var dragerID = 0;
    window.Drager = function ($element, options) {
        var that = this;
        var settings = $.extend(true, {
            preventDefault: true,

            mouse: true,
            touch: true,
            ignoreDistance: 10,
            momentumWeight: 500,
            momentumEasing: 'easeOutCubic',

            onMouseDown: $.noop,
            onStartDrag: $.noop,
            onDrag: $.noop,
            onStopDrag: $.noop,
            onMouseUp: $.noop
        }, options);

        var dragged = false;
        var inPreventArea = true;
        var dragging_allowed = false;
        var momentumPoints = [];
        var startPoint = null;
        that.id = dragerID++;

        var getEvent = function (event, type) {
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

            var evt = new DragerEvent({
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
            });

            if (type == 'start') {
                evt.dx = 0;
                evt.dy = 0;
                evt.startPoint = evt.point;
                return evt;
            } else if (type == 'stop') {
                evt.dx = getDx(startPoint, evt.point);
                evt.dy = getDy(startPoint, evt.point);
                evt.startPoint = startPoint;

                evt.momentum = {
                    weight: settings.momentumWeight,
                    easing: settings.momentumEasing,
                    startX: evt.dx,
                    startY: evt.dy,
                    speedX: 0,
                    speedY: 0,
                    duration: 0
                };

                return evt;
            } else {
                evt.dx = getDx(startPoint, evt.point);
                evt.dy = getDy(startPoint, evt.point);
                evt.startPoint = startPoint;
                return evt;
            }
        };

        var addMomentumPoint = function (evt) {
            var record = {
                point: evt.point,
                timeStamp: evt.timeStamp
            };

            if (momentumPoints.length == 2) {
                momentumPoints.shift();
            }
            momentumPoints.push(record);
        };

        var isMultiTouch = function (event) {
            var orig = event.originalEvent;
            var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
            return touchPoints.length > 1;
        };

        var startMomentumAnimation = function (evt) {
            var momentum = evt.momentum;
            var diffX = momentum.endX - momentum.startX;
            var diffY = momentum.endY - momentum.startY;
            that._momentumAnimation = $.animate({
                duration: momentum.duration,
                easing: momentum.easing,
                step: function (eProgress) {
                    evt.dx = momentum.startX + diffX * eProgress;
                    evt.dy = momentum.startY + diffY * eProgress;
                    evt.timeStamp = $.now();
                    settings.onDrag.call(that, evt);
                },
                complete: function () {
                    that._momentumAnimation = null;
                }
            });
        };

        that.stop = function (jumpToEnd) {
            if (that._momentumAnimation) {
                that._momentumAnimation.stop(jumpToEnd);
                that._momentumAnimation = null;
            }
        };

        // ================
        // === Handlers ===
        // ================
        var mouseDownHandler = function (event) {
            var evt = getEvent(event, 'start');
            dragged = false;
            inPreventArea = settings.ignoreDistance > 0;
            dragging_allowed = true;

            startPoint = evt.point;

            momentumPoints = [];
            addMomentumPoint(evt);

            return settings.onMouseDown.call(that, evt);
        };

        var dragHandler = function (event) {
            if (!dragging_allowed) return;

            var evt = getEvent(event, 'move');

            if (inPreventArea) {
                if (Math.max(Math.abs(evt.dx), Math.abs(evt.dy)) >= settings.ignoreDistance) {
                    inPreventArea = false;
                    startPoint = evt.point;
                }
                return
            }

            if (!dragged) {
                dragged = true;
                settings.onStartDrag.call(that, evt);
            }

            var lastMomentum = momentumPoints[momentumPoints.length - 1];
            if (evt.timeStamp - lastMomentum.timeStamp > 200) {
                addMomentumPoint(evt);
            }

            return settings.onDrag.call(that, evt);
        };

        var mouseUpHandler = function (event) {
            if (!dragging_allowed) return;
            dragging_allowed = false;

            var evt = getEvent(event, 'stop');

            if (dragged) {
                dragged = false;

                // Вычисление параметров инерции
                if (settings.momentumWeight) {
                    // Используем более старую точку, если последняя точка была
                    // совсем недавно.
                    var lastMomentum = momentumPoints[momentumPoints.length - 1];
                    if (evt.timeStamp - lastMomentum.timeStamp < 100) {
                        if (momentumPoints.length == 2) {
                            lastMomentum = momentumPoints[0];
                        }
                    }

                    evt.initMomentum(evt, lastMomentum);
                }

                settings.onStopDrag.call(that, evt);
            }

            var result = settings.onMouseUp.call(that, evt);
            if (evt.momentum && (evt.momentum.duration >= 100)) {
                startMomentumAnimation(evt);
            }
            return result;
        };


        that.detach = function() {
            // Отвязываем все события, связанные с объектом
            $element.off('.drager' + that.id);
            $(document).off('.drager' + that.id);
        };

        that.attach = function () {
            // Привязка обработчиков событий
            that.detach();

            // ====================
            // === Mouse Events ===
            // ====================
            if (settings.mouse) {
                // Блокируем дефолтовый Drag'n'Drop браузера
                if (settings.preventDefault) {
                    $element.on('dragstart.drager' + that.id, function () {
                        return false;
                    });
                }

                $element.on('mousedown.drager' + that.id, mouseDownHandler);
                $(document).on('mousemove.drager' + that.id, dragHandler);
                $(document).on('mouseup.drager' + that.id, mouseUpHandler);
            }

            // ====================
            // === Touch Events ===
            // ====================
            if (settings.touch) {
                $element.on('touchstart.drager' + that.id, function (event) {
                    if (isMultiTouch(event)) return;
                    return mouseDownHandler.call(this, event);
                });
                $(document).on('touchmove.drager' + that.id, function (event) {
                    if (isMultiTouch(event)) return;
                    return dragHandler.call(this, event);
                }).on('touchend.drager' + that.id, function (event) {
                    if (isMultiTouch(event)) return;
                    return mouseUpHandler.call(this, event);
                });
            }
        };

        // Инициализация
        that.attach();
    };

    $.drager = function ($root, options) {
        return new Drager($root, options);
    };

})(jQuery);