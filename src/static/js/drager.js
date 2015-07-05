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
            momentumLightness: 500            - "легкость" инерции (0 - нет инерции)
            momentumEasing: 'easeOutCubic'    - функция сглаживания иенрционного движения

            onMouseDown(event)                - нажатие мышью или тачпадом
            onStartDrag(event)                - начало перемещения
            onDrag(event)                     - процесс перемещения
            onStopDrag(event)                 - конец перемещения
            onMouseUp(event)                  - отпускание элемента

        Примеры:
            var drager = new Drager(element, {
                onMouseDown: function(evt) {
                    var $element = $(evt.target);

                    console.log('current point =', evt.point);

                    // блокировка всплытия события mousedown или touchstart
                    return false
                },
                onStartDrag: function(evt) {
                    var $element = $(evt.target);

                    console.log('Diff X =', Math.abs(evt.dx));
                    console.log('Diff Y =', Math.abs(evt.dy));
                    console.log('current point =', evt.point);
                },
                onDrag: function(evt) {
                    // тоже что в onStartDrag

                    // блокировка всплытия события mousemove или touchmove
                    return false
                },
                onStopDrag: function(evt) {
                    // предотвращение инерционного движения
                    evt.momentum = null;

                    // Модификация параметров инерционного движения
                    evt.momentum.setMomentumSpeed(undefined, 1);
                    evt.momentum.setMomentumLightness(600);
                    evt.momentum.setMomentumEndPoint(200, 400);
                    evt.momentum.setMomentumDuration(2000);
                    evt.momentum.setMomentumEasing('linear');
                },
                onMouseUp: function(evt) {
                    // тоже что в onStopDrag

                    // блокировка всплытия события mouseup или touchend
                    return false
                },
            });
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

    // ===============================================

    var DragerEvent = (function() {
        return function(event, drager) {
            this.origEvent = event;
            this.target = drager.$element.get(0);
            this.timeStamp = event.timeStamp;
            this.point = {
                pageX: event.pageX,
                pageY: event.pageY,
                clientX: event.clientX,
                clientY: event.clientY
            }
        };
    })();

    var MouseDownDragerEvent = (function(parent) {
        var MouseDownDragerEvent = function(event, drager) {
            parent.call(this, event, drager);

            this.dx = 0;
            this.dy = 0;
        };

        var _ = new Function;
        _.prototype = parent.prototype;
        _.prototype.constructor = _;
        return MouseDownDragerEvent;
    })(DragerEvent);

    var MouseMoveDragerEvent = (function(parent) {
        var MouseMoveDragerEvent = function(event, drager) {
            parent.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
        };

        var _ = new Function;
        _.prototype = parent.prototype;
        _.prototype.constructor = _;
        return MouseMoveDragerEvent;
    })(DragerEvent);

    var MouseUpDragerEvent = (function(parent) {
        var MouseUpDragerEvent = function(event, drager) {
            parent.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
            this.momentum = {
                lightness: drager.settings.momentumLightness,
                easing: drager.settings.momentumEasing,
                startX: this.dx,
                startY: this.dy,
                speedX: 0,
                speedY: 0,
                duration: 0
            };
        };

        MouseUpDragerEvent.prototype.autoCalcMomentum = function(evt, momentumPoint) {
            var dx = getDx(momentumPoint.point, evt.point);
            var dy = getDy(momentumPoint.point, evt.point);
            var duration = evt.origEvent.timeStamp - momentumPoint.timeStamp;

            this.setMomentumSpeed(dx / duration, dy / duration);
        };

        MouseUpDragerEvent.prototype.setMomentumSpeed = function(speedX, speedY) {
            if (typeof speedX != 'undefined') {
                this.momentum.speedX = speedX;
            }
            if (typeof speedY != 'undefined') {
                this.momentum.speedY = speedY;
            }

            var speed = Math.max(Math.abs(this.momentum.speedX), Math.abs(this.momentum.speedY));
            this.setMomentumDuration(speed * this.momentum.lightness);
        };

        MouseUpDragerEvent.prototype.setMomentumLightness = function(lightness) {
            this.momentum.lightness = lightness;

            var speed = Math.max(Math.abs(this.momentum.speedX), Math.abs(this.momentum.speedY));
            this.setMomentumDuration(speed * this.momentum.lightness);
        };

        MouseUpDragerEvent.prototype.setMomentumEndPoint = function(endX, endY) {
            var dx = endX - this.momentum.startX;
            var dy = endY - this.momentum.startY;
            var tx = this.momentum.speedX ? Math.abs(dx / this.momentum.speedX) : 0;
            var ty = this.momentum.speedY ? Math.abs(dy / this.momentum.speedY) : 0;

            this.momentum.duration = Math.max(tx, ty) || 0;
            this.momentum.endX = endX;
            this.momentum.endY = endY;
        };

        MouseUpDragerEvent.prototype.setMomentumDuration = function(duration) {
            this.momentum.duration = Math.abs(duration) || 0;
            this.momentum.endX = this.momentum.startX + this.momentum.speedX * this.momentum.duration;
            this.momentum.endY = this.momentum.startY + this.momentum.speedY * this.momentum.duration;
        };

        MouseUpDragerEvent.prototype.setMomentumEasing = function(easing) {
            this.momentum.easing = easing;
        };

        var _ = new Function;
        _.prototype = parent.prototype;
        _.prototype.constructor = _;
        return MouseUpDragerEvent;
    })(DragerEvent);

    // ===============================================

    window.Drager = (function() {
        var dragerID = 0;

        var isMultiTouch = function(event) {
            var orig = event.originalEvent;
            var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
            return touchPoints.length > 1;
        };

        var getTouchPoint = function(event) {
            var orig = event.originalEvent;
            if (typeof orig.changedTouches != 'undefined') {
                return orig.changedTouches[0]
            } else {
                return orig
            }
        };

        // Добавление контрольной точки, на основании которй будут вычисленены
        // параметры инерционного движения
        var addMomentumPoint = function(evt, pointsArray) {
            var record = {
                point: evt.point,
                timeStamp: evt.timeStamp
            };

            if (pointsArray.length == 2) {
                pointsArray.shift();
            }
            pointsArray.push(record);
        };

        // ================================================

        var Drager = function(element, options) {
            var $element = $(element).first();
            if (!$element.length) {
                console.error('Empty element for Drager');
                return
            }

            this.$element = $element;
            this.settings = $.extend(true, {
                preventDefault: true,

                mouse: true,
                touch: true,
                ignoreDistance: 10,
                momentumLightness: 500,
                momentumEasing: 'easeOutCubic',

                onMouseDown: $.noop,
                onStartDrag: $.noop,
                onDrag: $.noop,
                onStopDrag: $.noop,
                onMouseUp: $.noop
            }, options);


            this.id = dragerID++;

            // Был ли перемещен элемент (для обработки случаев клика и ignoreDistance)
            this.wasDragged = false;

            // Находимся ли мы в зоне ignoreDistance от начальной точки перетаскивания
            this._inPreventArea = true;

            // Защита от дублирования событий
            this._dragging_allowed = false;

            // Точки, на основани которых будет вычислена скорость инерциального движения
            this.momentumPoints = [];

            // Точка начала перемещения
            this.startPoint = null;

            // === Инициализация ===
            this.attach();
        };

        // Запуск инерционного движения
        Drager.prototype._startMomentumAnimation = function(evt) {
            var that = this;
            var momentum = evt.momentum;
            var diffX = momentum.endX - momentum.startX;
            var diffY = momentum.endY - momentum.startY;
            that._momentumAnimation = $.animate({
                duration: momentum.duration,
                easing: momentum.easing,
                step: function(eProgress) {
                    evt.dx = momentum.startX + diffX * eProgress;
                    evt.dy = momentum.startY + diffY * eProgress;
                    evt.timeStamp = $.now();
                    that.settings.onDrag.call(that, evt);
                },
                complete: function() {
                    that._momentumAnimation = null;
                }
            });
        };

        // Остановка инерционного движения
        Drager.prototype.stop = function(jumpToEnd) {
            if (this._momentumAnimation) {
                this._momentumAnimation.stop(jumpToEnd);
                this._momentumAnimation = null;
            }
        };

        // ================
        // === Handlers ===
        // ================

        Drager.prototype.mouseDownHandler = function(event) {
            var evt = new MouseDownDragerEvent(event, this);
            this.wasDragged = false;
            this._inPreventArea = this.settings.ignoreDistance > 0;
            this._dragging_allowed = true;

            this.startPoint = evt.point;

            this.momentumPoints = [];
            addMomentumPoint(evt, this.momentumPoints);

            return this.settings.onMouseDown.call(this, evt);
        };

        Drager.prototype.dragHandler = function(event) {
            if (!this._dragging_allowed) return;

            var evt = new MouseMoveDragerEvent(event, this);

            if (this._inPreventArea) {
                if (Math.max(Math.abs(evt.dx), Math.abs(evt.dy)) >= this.settings.ignoreDistance) {
                    this._inPreventArea = false;
                    this.startPoint = evt.point;
                }
                return
            }

            if (!this.wasDragged) {
                this.wasDragged = true;
                this.settings.onStartDrag.call(this, evt);
            }

            var lastMomentum = this.momentumPoints[this.momentumPoints.length - 1];
            if (evt.timeStamp - lastMomentum.timeStamp > 200) {
                addMomentumPoint(evt, this.momentumPoints);
            }

            return this.settings.onDrag.call(this, evt);
        };

        Drager.prototype.mouseUpHandler = function(event) {
            if (!this._dragging_allowed) return;
            this._dragging_allowed = false;

            var evt = new MouseUpDragerEvent(event, this);

            if (this.wasDragged) {
                this.wasDragged = false;

                // Вычисление параметров инерции
                if (this.settings.momentumLightness > 0) {
                    // Используем более старую точку, если последняя точка была
                    // совсем недавно.
                    var lastMomentum = this.momentumPoints[this.momentumPoints.length - 1];
                    if (evt.timeStamp - lastMomentum.timeStamp < 100) {
                        if (this.momentumPoints.length == 2) {
                            lastMomentum = this.momentumPoints[0];
                        }
                    }

                    evt.autoCalcMomentum(evt, lastMomentum);
                }

                this.settings.onStopDrag.call(this, evt);
            }

            var result = this.settings.onMouseUp.call(this, evt);
            if (evt.momentum && (evt.momentum.duration >= 100)) {
                this._startMomentumAnimation(evt);
            }
            return result;
        };

        // ================
        // ==== Events ====
        // ================

        // Удаление обработчиков событий
        Drager.prototype.detach = function() {
            // Отвязываем все события, связанные с объектом
            this.$element.off('.drager' + this.id);
            $(document).off('.drager' + this.id);
        };

        // Привязка обработчиков событий
        Drager.prototype.attach = function() {
            var that = this;

            this.detach();

            // ====================
            // === Mouse Events ===
            // ====================
            if (this.settings.mouse) {
                // Блокируем дефолтовый Drag'n'Drop браузера
                if (this.settings.preventDefault) {
                    this.$element.on('dragstart.drager' + this.id, function() {
                        return false;
                    });
                }

                this.$element.on('mousedown.drager' + this.id, function() {
                    return that.mouseDownHandler.call(that, event);
                });
                $(document).on('mousemove.drager' + this.id, function() {
                    return that.dragHandler.call(that, event);
                }).on('mouseup.drager' + this.id, function() {
                    return that.mouseUpHandler.call(that, event);
                });
            }

            // ====================
            // === Touch Events ===
            // ====================
            if (this.settings.touch) {
                this.$element.on('touchstart.drager' + this.id, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseDownHandler.call(that, getTouchPoint(event));
                });
                $(document).on('touchmove.drager' + this.id, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.dragHandler.call(that, getTouchPoint(event));
                }).on('touchend.drager' + this.id, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseUpHandler.call(that, getTouchPoint(event));
                });
            }
        };

        return Drager;
    })();

})(jQuery);