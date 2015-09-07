(function($) {

    /*
        Генерирует события перетаскивания. Реального перемещения не делает.
        Это только интерфейс для реализации разных штук.
        Есть настройки для реализации продолжения движения по инерции
        при отпускании кнопки мыши.

        Требует:
            jquery.utils.js

        Параметры:
            preventDefaultDrag: true/false    - предотвратить событие drag по-умолчанию
            mouse: true                       - разрешить перетаскивание мышью
            touch: true                       - разрешить перетаскивание тачпадом
            ignoreDistance: 10                - игнорировать краткие движения
            momentum: true                    - добавлять движение по инерции
            momentumLightness: 500            - "легкость" инерции (0 - нет инерции)
            momentumEasing: 'easeOutCubic'    - функция сглаживания иенрционного движения

            onMouseDown(event)                - нажатие мышью или тачпадом
            onStartDrag(event)                - начало перемещения
            onDrag(event)                     - процесс перемещения
            onSetMomentum(event, momentum)    - для модификации параметров инерции
            onStopDrag(event)                 - конец перемещения
            onMouseUp(event)                  - отпускание элемента
            onMomentumStarted(momentum)       - инерция запущена
            onMomentumStopped(completed)      - остановка инерции

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

                    console.log('Diff X =', evt.abs_dx);
                    console.log('Diff Y =', evt.abs_dy);
                    console.log('current point =', evt.point);
                },
                onDrag: function(evt) {
                    // тоже что в onStartDrag

                    // блокировка всплытия события mousemove или touchmove
                    return false
                },
                onSetMomentum: function(evt, momentum) {
                    // предотвращение инерционного движения
                    return false;

                    // Модификация параметров инерционного движения
                    momentum.setSpeed(undefined, 1);
                    momentum.setLightness(600);
                    momentum.setEndPoint(200, 400);
                    momentum.setDuration(2000);
                    momentum.setEasing('linear');
                    return momentum;
                },
                onStopDrag: function(evt, momentum) {
                    if (!momentum) {
                        // не будет инерции
                    }
                },
                onMouseUp: function(evt, momentum) {
                    if (!momentum) {
                        // не будет инерции
                    }

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

    // ===============================================

    var Momentum = (function() {
        var Momentum = function(drager, event, momentumPoint) {
            this.lightness = drager.settings.momentumLightness;
            this.easing = drager.settings.momentumEasing;
            this.startX = event.dx;
            this.startY = event.dy;
            this.speedX = 0;
            this.speedY = 0;
            this.duration = 0;

            var dx = getDx(momentumPoint.point, event.point);
            var dy = getDy(momentumPoint.point, event.point);
            var duration = event.origEvent.timeStamp - momentumPoint.timeStamp;
            this.setSpeed(dx / duration, dy / duration);
        };

        Momentum.prototype.setSpeed = function(speedX, speedY) {
            if (typeof speedX != 'undefined') {
                this.speedX = speedX;
            }
            if (typeof speedY != 'undefined') {
                this.speedY = speedY;
            }

            var speed = Math.max(Math.abs(this.speedX), Math.abs(this.speedY));
            this.setDuration(speed * this.lightness);
        };

        Momentum.prototype.setDuration = function(duration) {
            this.duration = Math.abs(duration) || 0;
            this.endX = this.startX + this.speedX * this.duration;
            this.endY = this.startY + this.speedY * this.duration;
        };

        Momentum.prototype.setLightness = function(lightness) {
            this.lightness = lightness;

            var speed = Math.max(Math.abs(this.speedX), Math.abs(this.speedY));
            this.setDuration(speed * this.lightness);
        };

        Momentum.prototype.setEndPoint = function(endX, endY) {
            var dx = endX - this.startX;
            var dy = endY - this.startY;
            var tx = this.speedX ? Math.abs(dx / this.speedX) : 0;
            var ty = this.speedY ? Math.abs(dy / this.speedY) : 0;

            this.duration = Math.max(tx, ty) || 0;
            this.endX = endX;
            this.endY = endY;
        };

        Momentum.prototype.setEasing = function(easing) {
            this.easing = easing;
        };

        return Momentum;
    })();

    // ===============================================

    var DragerEvent = (function() {
        return function(event, drager) {
            var mouseEvent = event;
            if (event.type.substr(0, 5) == 'touch') {
                mouseEvent = getTouchPoint(event);
            }

            this.origEvent = event;
            this.target = drager.$element.get(0);
            this.timeStamp = event.timeStamp;
            this.point = {
                pageX: mouseEvent.pageX,
                pageY: mouseEvent.pageY,
                clientX: mouseEvent.clientX,
                clientY: mouseEvent.clientY
            }
        };
    })();

    var MouseDownDragerEvent = (function(parent) {
        var MouseDownDragerEvent = function(event, drager) {
            parent.call(this, event, drager);

            this.dx = 0;
            this.dy = 0;
            this.abs_dx = 0;
            this.abs_dy = 0;
        };

        var _ = function() { this.constructor = MouseDownDragerEvent; };
        _.prototype = parent.prototype;
        MouseDownDragerEvent.prototype = new _;

        return MouseDownDragerEvent;
    })(DragerEvent);

    var MouseMoveDragerEvent = (function(parent) {
        var MouseMoveDragerEvent = function(event, drager) {
            parent.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
            this.abs_dx = Math.abs(this.dx);
            this.abs_dy = Math.abs(this.dy);
        };

        var _ = function() { this.constructor = MouseMoveDragerEvent; };
        _.prototype = parent.prototype;
        MouseMoveDragerEvent.prototype = new _;

        return MouseMoveDragerEvent;
    })(DragerEvent);

    var MouseUpDragerEvent = (function(parent) {
        var MouseUpDragerEvent = function(event, drager) {
            parent.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
            this.abs_dx = Math.abs(this.dx);
            this.abs_dy = Math.abs(this.dy);
        };

        var _ = function() { this.constructor = MouseUpDragerEvent; };
        _.prototype = parent.prototype;
        MouseUpDragerEvent.prototype = new _;

        return MouseUpDragerEvent;
    })(DragerEvent);

    // ===============================================

    window.Drager = (function() {
        var dragerID = 0;

        // ================================================

        var Drager = function(element, options) {
            this.$element = $.findFirstElement(element);
            if (!this.$element.length) {
                console.error('Empty element for Drager');
                return
            }

            this.settings = $.extend(true, {
                preventDefault: true,

                mouse: true,
                touch: true,
                ignoreDistance: 10,
                momentum: true,
                momentumLightness: 500,
                momentumEasing: 'easeOutCubic',
                minMomentumDuration: 100,

                onMouseDown: $.noop,
                onStartDrag: $.noop,
                onDrag: $.noop,
                onStopDrag: $.noop,
                onSetMomentum: function(evt, momentum) { return momentum },
                onMouseUp: $.noop,
                onMomentumStarted: $.noop,
                onMomentumStopped: $.noop
            }, options);


            this.id = dragerID++;

            // Был ли перемещен элемент (для обработки случаев клика и ignoreDistance)
            this.wasDragged = false;

            // Находимся ли мы в зоне ignoreDistance от начальной точки перетаскивания
            this._inPreventArea = true;

            // Защита от дублирования событий
            this._dragging_allowed = false;

            // Точки, на основани которых будет вычислена скорость инерциального движения
            this._momentumPoints = [];

            // Точка начала перемещения
            this.startPoint = null;

            // === Инициализация ===
            this.attach();
        };

        // Добавление точки вычисления инерции
        Drager.prototype._addMomentumPoint = function(evt) {
            if (this._momentumPoints.length) {
                // Если недавно уже добавляли - выходим
                var lastPoint = this._momentumPoints[this._momentumPoints.length - 1];
                if (evt.timeStamp - lastPoint.timeStamp < 200) {
                    return
                }
            }

            var record = {
                point: evt.point,
                timeStamp: evt.timeStamp
            };

            if (this._momentumPoints.length == 2) {
                this._momentumPoints.shift();
            }
            this._momentumPoints.push(record);
        };

        // Получение точки вычисления инерции
        Drager.prototype._getMomentumPoint = function(evt) {
            if (!this._momentumPoints.length) {
                return
            }

            var lastPoint = this._momentumPoints[this._momentumPoints.length - 1];
            if (evt.timeStamp - lastPoint.timeStamp < 100) {
                if (this._momentumPoints.length == 2) {
                    lastPoint = this._momentumPoints[0];
                }
            }
            return lastPoint;
        };

        // Запуск инерционного движения
        Drager.prototype.startMomentum = function(evt, momentum) {
            var that = this;
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
                    that.settings.onMomentumStopped.call(that, true);
                }
            });
        };

        // Остановка инерционного движения
        Drager.prototype.stopMomentum = function(jumpToEnd) {
            if (this._momentumAnimation) {
                this._momentumAnimation.stop(jumpToEnd);
                this._momentumAnimation = null;
                this.settings.onMomentumStopped.call(this, false);
            }
        };

        // Сброс начала отсчета передвижения
        Drager.prototype.setStartPoint = function(evt) {
            this.startPoint = evt.point;
        };
        
        // Прекращения отслеживания текущего сеанса перемещения
        Drager.prototype.stopCurrent = function(evt) {
            var momentum;
            this._dragging_allowed = false;
            
            if (this.wasDragged) {
                this.wasDragged = false;

                // Вычисление параметров инерции
                if (this.settings.momentum) {
                    var lastPoint = this._getMomentumPoint(evt);
                    if (lastPoint) {
                        momentum = new Momentum(this, evt, lastPoint);
                        momentum = this.settings.onSetMomentum.call(this, evt, momentum);
                        if (!momentum || (momentum.duration < this.settings.minMomentumDuration)) {
                            momentum = null;
                        }
                    }
                }

                this.settings.onStopDrag.call(this, evt, momentum);
            }

            var result = this.settings.onMouseUp.call(this, evt, momentum);

            // запуск инерции
            if (momentum) {
                this.startMomentum(evt, momentum);
                this.settings.onMomentumStarted.call(this, momentum);
            }

            return result;
        };
        
        // ================
        // === Handlers ===
        // ================

        Drager.prototype.mouseDownHandler = function(event) {
            var evt = new MouseDownDragerEvent(event, this);
            this.wasDragged = false;
            this._inPreventArea = this.settings.ignoreDistance > 0;
            this._dragging_allowed = true;
            this._momentumPoints = [];
            this._addMomentumPoint(evt);

            this.setStartPoint(evt);
            return this.settings.onMouseDown.call(this, evt);
        };

        Drager.prototype.dragHandler = function(event) {
            if (!this._dragging_allowed) return;

            var evt = new MouseMoveDragerEvent(event, this);

            if (this._inPreventArea) {
                if (Math.max(evt.abs_dx, evt.abs_dy) >= this.settings.ignoreDistance) {
                    this._inPreventArea = false;
                    this.setStartPoint(evt);
                }
                return
            }

            if (!this.wasDragged) {
                this.wasDragged = true;
                this.settings.onStartDrag.call(this, evt);
            }

            this._addMomentumPoint(evt);

            return this.settings.onDrag.call(this, evt);
        };

        Drager.prototype.mouseUpHandler = function(event) {
            if (!this._dragging_allowed) return;
            
            var evt = new MouseUpDragerEvent(event, this);
            return this.stopCurrent(evt);
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

                this.$element.on('mousedown.drager' + this.id, function(event) {
                    return that.mouseDownHandler.call(that, event);
                });
                $(document).on('mousemove.drager' + this.id, function(event) {
                    return that.dragHandler.call(that, event);
                }).on('mouseup.drager' + this.id, function(event) {
                    return that.mouseUpHandler.call(that, event);
                });
            }

            // ====================
            // === Touch Events ===
            // ====================
            if (this.settings.touch) {
                this.$element.on('touchstart.drager' + this.id, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseDownHandler.call(that, event);
                });
                $(document).on('touchmove.drager' + this.id, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.dragHandler.call(that, event);
                }).on('touchend.drager' + this.id, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseUpHandler.call(that, event);
                });
            }
        };

        return Drager;
    })();

})(jQuery);
