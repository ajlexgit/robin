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
            ignoreDistanceX: 18               - игнорировать краткие движения по оси X
            ignoreDistanceY: 18               - игнорировать краткие движения по оси Y
            momentum: true                    - добавлять движение по инерции
            momentumLightness: 500            - "легкость" инерции (0 - нет инерции)
            momentumEasing: 'easeOutCubic'    - функция сглаживания иенрционного движения

            onMouseDown(event)                - нажатие мышью или тачпадом
            onStartDrag(event)                - начало перемещения. Если вернет false, перемещение не начнется
            onDrag(event)                     - процесс перемещения
            onSetMomentum(event, momentum)    - для модификации параметров инерции
            onStopDrag(event)                 - конец перемещения
            onMouseUp(event)                  - отпускание элемента
            onMomentumStarted(momentum)       - инерция запущена
            onMomentumStopped(completed)      - остановка инерции

        Примеры:
            var drager = Drager.create(element, {
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

                    // отмена перемещения
                    return false
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

    /*
        Движение по инерции
     */
    var Momentum = Class(null, function Momentum(cls, superclass) {
        cls.prototype.init = function(drager, event, momentumPoint) {
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

        cls.prototype.setSpeed = function(speedX, speedY) {
            if (typeof speedX != 'undefined') {
                this.speedX = speedX;
            }
            if (typeof speedY != 'undefined') {
                this.speedY = speedY;
            }

            var speed = Math.max(Math.abs(this.speedX), Math.abs(this.speedY));
            this.setDuration(speed * this.lightness);
        };

        cls.prototype.setDuration = function(duration) {
            this.duration = Math.abs(duration) || 0;
            this.endX = this.startX + this.speedX * this.duration;
            this.endY = this.startY + this.speedY * this.duration;
        };

        cls.prototype.setLightness = function(lightness) {
            this.lightness = lightness;

            var speed = Math.max(Math.abs(this.speedX), Math.abs(this.speedY));
            this.setDuration(speed * this.lightness);
        };

        cls.prototype.setEndPoint = function(endX, endY) {
            var dx = endX - this.startX;
            var dy = endY - this.startY;
            var tx = this.speedX ? Math.abs(dx / this.speedX) : 0;
            var ty = this.speedY ? Math.abs(dy / this.speedY) : 0;

            this.duration = Math.max(tx, ty) || 0;
            this.endX = endX;
            this.endY = endY;
        };

        cls.prototype.setEasing = function(easing) {
            this.easing = easing;
        };
    });

    // ===============================================

    var DragerEvent = Class(null, function DragerEvent(cls, superclass) {
        cls.prototype.init = function(event, drager) {
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
    });

    var MouseDownDragerEvent = Class(DragerEvent, function MouseDownDragerEvent(cls, superclass) {
        cls.prototype.init = function(event, drager) {
            superclass.prototype.init.call(this, event, drager);

            this.dx = 0;
            this.dy = 0;
            this.abs_dx = 0;
            this.abs_dy = 0;
        };
    });

    var MouseMoveDragerEvent = Class(DragerEvent, function MouseMoveDragerEvent(cls, superclass) {
        cls.prototype.init = function(event, drager) {
            superclass.prototype.init.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
            this.abs_dx = Math.abs(this.dx);
            this.abs_dy = Math.abs(this.dy);
        };
    });

    var MouseUpDragerEvent = Class(DragerEvent, function MouseUpDragerEvent(cls, superclass) {
        cls.prototype.init = function(event, drager) {
            superclass.prototype.init.call(this, event, drager);

            this.dx = getDx(drager.startPoint, this.point);
            this.dy = getDy(drager.startPoint, this.point);
            this.abs_dx = Math.abs(this.dx);
            this.abs_dy = Math.abs(this.dy);
        };
    });

    // ===============================================

    var dragerID = 0;
    window.Drager = Class(null, function Drager(cls, superclass) {
        cls.prototype.init = function(element, options) {
            this.$element = $(element).first();
            if (!this.$element.length) {
                return this.raise('root element not found');
            }

            this.opts = $.extend({
                preventDefault: true,

                mouse: true,
                touch: true,
                ignoreDistanceX: 18,
                ignoreDistanceY: 18,
                momentum: true,
                momentumLightness: 500,
                momentumEasing: 'easeOutCubic',
                minMomentumDuration: 100,

                onMouseDown: $.noop,
                onStartDrag: $.noop,
                onDrag: $.noop,
                onStopDrag: $.noop,
                onSetMomentum: function(evt, momentum) {
                    return momentum
                },
                onMouseUp: $.noop,
                onMomentumStarted: $.noop,
                onMomentumStopped: $.noop
            }, options);


            this.id = dragerID++;

            // Был ли перемещен элемент (для обработки случаев клика и ignoreDistance)
            this.wasDragged = false;

            // Защита от дублирования событий
            this._dragging_allowed = false;

            // Точки, на основани которых будет вычислена скорость инерциального движения
            this._momentumPoints = [];

            // Точка начала перемещения
            this.startPoint = null;

            // === Инициализация ===
            this.attach();
        };

        // ================================================

        /*
            Добавление точки вычисления инерции
         */
        cls.prototype._addMomentumPoint = function(evt) {
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

        /*
            Получение точки вычисления инерции
         */
        cls.prototype._getMomentumPoint = function(evt) {
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

        /*
            Запуск инерционного движения
          */
        cls.prototype.startMomentum = function(evt, momentum) {
            var that = this;
            that._momentumAnimation = $.animate({
                duration: momentum.duration,
                easing: momentum.easing,
                init: function() {
                    this.autoInit('x', momentum.startX, momentum.endX);
                    this.autoInit('y', momentum.startY, momentum.endY);
                },
                step: function(eProgress) {
                    evt.dx = this.autoCalc('x', eProgress);
                    evt.dy = this.autoCalc('y', eProgress);
                    evt.timeStamp = $.now();
                    that.opts.onDrag.call(that, evt);
                },
                complete: function() {
                    that._momentumAnimation = null;
                    that.opts.onMomentumStopped.call(that, true);
                }
            });
        };

        /*
            Остановка инерционного движения
          */
        cls.prototype.stopMomentum = function(jumpToEnd) {
            if (this._momentumAnimation) {
                this._momentumAnimation.stop(jumpToEnd);
                this._momentumAnimation = null;
                this.opts.onMomentumStopped.call(this, false);
            }
        };

        /*
            Сброс начала отсчета передвижения
          */
        cls.prototype.setStartPoint = function(evt) {
            this.startPoint = evt.point;
        };

        /*
            Прекращения отслеживания текущего сеанса перемещения
          */
        cls.prototype.stopCurrent = function(evt) {
            var momentum;
            this._dragging_allowed = false;

            if (this.wasDragged) {
                this.wasDragged = false;

                // Вычисление параметров инерции
                if (this.opts.momentum) {
                    var lastPoint = this._getMomentumPoint(evt);
                    if (lastPoint) {
                        momentum = Momentum.create(this, evt, lastPoint);
                        momentum = this.opts.onSetMomentum.call(this, evt, momentum);
                        if (!momentum || (momentum.duration < this.opts.minMomentumDuration)) {
                            momentum = null;
                        }
                    }
                }

                this.opts.onStopDrag.call(this, evt, momentum);
            }

            var result = this.opts.onMouseUp.call(this, evt, momentum);

            // запуск инерции
            if (momentum) {
                this.startMomentum(evt, momentum);
                this.opts.onMomentumStarted.call(this, momentum);
            }

            return result;
        };

        // ================
        // === Handlers ===
        // ================

        cls.prototype.mouseDownHandler = function(event) {
            var evt = MouseDownDragerEvent.create(event, this);
            this.wasDragged = false;
            this._dragging_allowed = true;
            this._momentumPoints = [];
            this._addMomentumPoint(evt);

            this.setStartPoint(evt);
            return this.opts.onMouseDown.call(this, evt);
        };

        cls.prototype.dragHandler = function(event) {
            if (!this._dragging_allowed) return;

            var evt = MouseMoveDragerEvent.create(event, this);
            this._addMomentumPoint(evt);

            if (!this.wasDragged) {
                if ((evt.abs_dx > this.opts.ignoreDistanceX) || (evt.abs_dy > this.opts.ignoreDistanceY)) {
                    var allowed = this.opts.onStartDrag.call(this, evt);
                    if (allowed === false) {
                        return
                    }
                    this.wasDragged = true;
                } else {
                    return;
                }
            }

            return this.opts.onDrag.call(this, evt);
        };

        cls.prototype.mouseUpHandler = function(event) {
            if (!this._dragging_allowed) return;

            var evt = MouseUpDragerEvent.create(event, this);
            return this.stopCurrent(evt);
        };

        // ================
        // ==== Events ====
        // ================

        // Удаление обработчиков событий
        cls.prototype.detach = function() {
            // Отвязываем все события, связанные с объектом
            this.$element.off('.drager' + this.id);
            $(document).off('.drager' + this.id);
        };

        // Привязка обработчиков событий
        cls.prototype.attach = function() {
            var that = this;

            this.detach();

            // ====================
            // === Mouse Events ===
            // ====================
            if (this.opts.mouse) {
                // Блокируем дефолтовый Drag'n'Drop браузера
                if (this.opts.preventDefault) {
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
            if (this.opts.touch) {
                var ns = 'drager' + this.id;

                var touchstart = window.navigator.msPointerEnabled ? 'MSPointerDown' : 'touchstart';
                var touchmove = window.navigator.msPointerEnabled ? 'MSPointerMove' : 'touchmove';
                var touchend = window.navigator.msPointerEnabled ? 'MSPointerUp' : 'touchend';

                this.$element.on(touchstart + '.' + ns, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseDownHandler.call(that, event);
                });
                $(document).on(touchmove + '.' + ns, function(event) {
                    if (isMultiTouch(event)) return;
                    return that.dragHandler.call(that, event);
                }).on(touchend + '.' + ns , function(event) {
                    if (isMultiTouch(event)) return;
                    return that.mouseUpHandler.call(that, event);
                });
            }
        };
    });

})(jQuery);
