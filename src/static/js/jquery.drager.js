(function($) {

    /*
        Генерирует события перетаскивания.

        Параметры:
            preventDefaultDrag: true/false    - предотвратить Drag по-умолчанию
            momentumWeight: 500               - величина инерции

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

    var DragerEvent = function(properties) {
        $.extend(true, this, properties);

        this.initMomentum = function(evt, lastMomentumRecord) {
            var dx = getDx(lastMomentumRecord.point, evt.point);
            var dy = getDy(lastMomentumRecord.point, evt.point);
            var duration = event.timeStamp - lastMomentumRecord.timeStamp;

            this.setMomentumSpeed(dx / duration, dy / duration);
        };

        this.setMomentumSpeed = function(speedX, speedY) {
            if (typeof speedX != 'undefined') {
                this.momentum.speedX = speedX;
            }
            if (typeof speedY != 'undefined') {
                this.momentum.speedY = speedY;
            }

            var speed = Math.max(Math.abs(this.momentum.speedX), Math.abs(this.momentum.speedY));
            this.setMomentumDuration(speed * this.momentum.weight);
        };

        this.setMomentumWeight = function(weight) {
            this.momentum.weight = weight;

            var speed = Math.max(Math.abs(this.momentum.speedX), Math.abs(this.momentum.speedY));
            this.setMomentumDuration(speed * this.momentum.weight);
        };

        this.setMomentumPoint = function(endX, endY) {
            var dx = endX - this.momentum.startX;
            var dy = endY - this.momentum.startY;
            var tx = this.momentum.speedX ? Math.abs(dx / this.momentum.speedX) : 0;
            var ty = this.momentum.speedY ? Math.abs(dy / this.momentum.speedY) : 0;

            this.momentum.duration = Math.max(tx, ty) || 0;
            this.momentum.endX = endX;
            this.momentum.endY = endY;
        };

        this.setMomentumDuration = function(duration) {
            this.momentum.duration = Math.abs(duration) || 0;
            this.momentum.endX = this.momentum.startX + this.momentum.speedX * this.momentum.duration;
            this.momentum.endY = this.momentum.startY + this.momentum.speedY * this.momentum.duration;
        };

        this.setMomentumEasing = function(easing) {
            this.momentum.easing = easing;
        };
    };

    window.Drager = function($element, options) {
        var that = this;
        var settings = $.extend(true, {
            preventDefault: true,

            mouse: true,
            touch: true,
            momentumWeight: 500,
            momentumEasing: 'easeOutCubic',

            onStartDrag: $.noop,
            onDrag: $.noop,
            onStopDrag: $.noop
        }, options);

        that._momentumPoints = [];
        that.dragging = false;
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
                evt.dx = getDx(that.startPoint, evt.point);
                evt.dy = getDy(that.startPoint, evt.point);
                evt.startPoint = that.startPoint;

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
                evt.dx = getDx(that.startPoint, evt.point);
                evt.dy = getDy(that.startPoint, evt.point);
                evt.startPoint = that.startPoint;
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

        that.animateMomentum = function(evt, options) {
            var animationStart = $.now();
            var diffX = evt.momentum.endX - evt.momentum.startX;
            var diffY = evt.momentum.endY - evt.momentum.startY;
            that._momentumTimer = setInterval(function() {
                var progress = ($.now() - animationStart) / options.duration;
                if (progress >= 1) {
                    progress = 1;
                    clearInterval(that._momentumTimer);
                }

                progress = $.easing[options.easing](progress);
                
                evt.dx = evt.momentum.startX + diffX * progress;
                evt.dy = evt.momentum.startY + diffY * progress;
                evt.timeStamp = $.now();
                settings.onDrag.call(that, evt);
            }, 20);
        };

        that.stopMomentumAnimation = function() {
            if (that._momentumTimer) {
                clearInterval(that._momentumTimer);
            }
        };
        
        // ================
        // === Handlers ===
        // ================
        var startDragHandler = function(event) {
            that.stopMomentumAnimation();
            
            var evt = that.getEvent(event, 'start');
            that.dragging = true;
            that.startPoint = evt.point;

            that._momentumPoints = [];
            that.addMomentumPoint(evt);

            return settings.onStartDrag.call(that, evt);
        };

        var dragHandler = function(event) {
            if (!that.dragging) return;

            var evt = that.getEvent(event, 'move');

            var lastMomentum = that._momentumPoints[that._momentumPoints.length - 1];
            if (evt.timeStamp - lastMomentum.timeStamp > 200) {
                that.addMomentumPoint(evt);
            }

            return settings.onDrag.call(that, evt);
        };

        var stopDragHandler = function(event) {
            if (!that.dragging) return;
            that.dragging = false;

            var evt = that.getEvent(event, 'stop');

            // Вычисление параметров инерции
            if (settings.momentumWeight) {
                // Используем более старую точку, если последняя точка была
                // совсем недавно.
                var lastMomentum = that._momentumPoints[that._momentumPoints.length - 1];
                if (evt.timeStamp - lastMomentum.timeStamp < 100) {
                    if (that._momentumPoints.length == 2) {
                        lastMomentum = that._momentumPoints[0];
                    }
                }

                evt.initMomentum(evt, lastMomentum);
            }

            var result = settings.onStopDrag.call(that, evt);
            if (evt.momentum && (evt.momentum.duration >= 100)) {
                that.animateMomentum(evt, {
                    duration: evt.momentum.duration,
                    easing: evt.momentum.easing
                });
            }
            return result;
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