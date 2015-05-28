(function($) {

    /*
        Генерирует события перетаскивания.

        Параметры:
            mouse:
                preventDefaultDrag: true/false    - предотвратить Drag по-умолчанию
                speedInterval: 50                 - интервал обновления скорости мыши
                deceleration: [0-1]               - показатель плавности изменения скорости:
                                                    0 - резкое изменение
                                                    1 - отсутсвие изменения

                onStartDrag(event)                - начало перетаскивания. Если вернет false,
                                                    перетасквание будет отменено.
                onDrag(event, dX, dY, speed)      - процесс перемещения
                onStopDrag(event, dX, dY, speed)  - конец перемещения

            touch:
    */

    var current = null;
    var mousePosX, mousePosY;
    var mouseLastPosX = -1;
    var mouseLastPosY = -1;
    var mouseDistance = 0;
    var mouseSpeed = 0;
    var mouseSpeedTimer;

    window.Drager = function($element, options) {
        var that = this;
        var settings = $.extend(true, {
            mouse: {
                preventDefaultDrag: true,
                speedInterval: 100,
                deceleration: 0.66,
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

        // Обновление расстояния, пройденного мышью
        var updateMouseDistance = function(event) {
            if (mouseLastPosX > -1) {
                mouseDistance += Math.sqrt(
                    Math.pow(event.pageX - mouseLastPosX, 2) +
                    Math.pow(event.pageY - mouseLastPosY, 2)
                );
            }
            mouseLastPosX = event.pageX;
            mouseLastPosY = event.pageY;
        };

        // === MOUSE ===
        if (settings.mouse) {
            // Блокируем дефолтовый Drag'n'Drop браузера
            if (settings.mouse.preventDefaultDrag) {
                $element.on('dragstart.drager', function() {
                    return false;
                });
            }

            $element.on('mousedown.drager', function(event) {
                if (settings.mouse.onStartDrag.call(this, event) === false) {
                    return;
                }

                current = this;
                mousePosX = event.pageX;
                mousePosY = event.pageY;

                mouseSpeed = 0;
                mouseDistance = 0;
                mouseSpeedTimer = setInterval(function() {
                    var newSpeed = (1000 * mouseDistance) / settings.mouse.speedInterval;
                    mouseSpeed = Math.round(
                        settings.mouse.deceleration * mouseSpeed +
                        (1 - settings.mouse.deceleration) * newSpeed
                    );
                    mouseDistance = 0;
                }, settings.mouse.speedInterval);
            });

            $(document).on('mousemove.drager', function(event) {
                if (!current) return;

                var dX = event.pageX - mousePosX;
                var dY = event.pageY - mousePosY;

                updateMouseDistance(event);

                settings.mouse.onDrag.call(current, event, dX, dY, mouseSpeed);
            }).on('mouseup.drager', function(event) {
                current = null;

                var dX = event.pageX - mousePosX;
                var dY = event.pageY - mousePosY;

                updateMouseDistance(event);
                clearInterval(mouseSpeedTimer);

                settings.mouse.onStopDrag.call(current, event, dX, dY, mouseSpeed);
            });
        }

        // === TOUCH ===
        if (settings.touch) {
            $element.on('touchstart.drager', function (event) {
                if (settings.mouse.onStartDrag.call(this, event) === false) {
                    return;
                }

                current = this;
                mousePosX = event.pageX;
                mousePosY = event.pageY;

                mouseSpeed = 0;
                mouseDistance = 0;
                mouseSpeedTimer = setInterval(function () {
                    var newSpeed = (1000 * mouseDistance) / settings.mouse.speedInterval;
                    mouseSpeed = Math.round(
                        settings.mouse.deceleration * mouseSpeed +
                        (1 - settings.mouse.deceleration) * newSpeed
                    );
                    mouseDistance = 0;
                }, settings.mouse.speedInterval);
            });

            $(document).on('mousemove.drager', function (event) {
                if (!current) return;

                var dX = event.pageX - mousePosX;
                var dY = event.pageY - mousePosY;

                updateMouseDistance(event);

                settings.mouse.onDrag.call(current, event, dX, dY, mouseSpeed);
            }).on('mouseup.drager', function (event) {
                current = null;

                var dX = event.pageX - mousePosX;
                var dY = event.pageY - mousePosY;

                updateMouseDistance(event);
                clearInterval(mouseSpeedTimer);

                settings.mouse.onStopDrag.call(current, event, dX, dY, mouseSpeed);
            });
        }
    };

})(jQuery);