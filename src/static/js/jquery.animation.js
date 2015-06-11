(function($) {

    /*
        $.animation_frame
            Обертка requestAnimationFrame для функций, работающих с CSS-анимацией.

        $.animation
            Кастомная JS-анимация. Главным образом предназначена для
            анимации CSS3-свойств, которые не поддерживаются jQuery.

            Есть возможность поставить анимацию на паузу.

            Параметры:
                duration: 1000                          - длительность анимации
                delay: 20                               - частота фреймов анимации
                easing: 'linear'                        - функция сглаживания
                paused: false                           - создать приостановленной

                init: $.noop                            - callback инициализации
                step: function(eProgress)               - шаг анимации
                start: $.noop                           - callback запуска анимации
                stop: $.noop                            - callback остановки анимации
                complete: $.noop                        - callback полного завершения анимации

            Методы:
                start()     - запуск анимации
                stop()      - приостановить анимацию
                reset()     - сбросить прогресс анимации
    */

    var handler = window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function (callback) {
            window.setTimeout(callback, 1000 / 60);
        };

    $.animation_frame = function (callback, element) {
        return $.proxy(handler, window, callback, element)
    };


    function Animation(options) {
        var that = this;
        that.paused = true;
        that.settings = $.extend({
            duration: 1000,
            delay: 20,
            easing: 'linear',
            paused: false,

            init: $.noop,
            step: $.noop,
            start: $.noop,
            stop: $.noop,
            complete: $.noop
        }, options);

        var applyProgress = function () {
            // Применение шага анимации (для уже установленного that.progress)
            var easeProgress = $.easing[that.settings.easing](that.progress);
            that.settings.step.call(that, easeProgress);

            if (that.progress === 1) {
                that.stop();
                that.settings.complete.call(that);
            }
        };

        var timerHandle = function () {
            // Применение шага анимации с вычислением that.progress
            that.progress = ($.now() - that._start) / that.duration;
            if (that.progress >= 1) {
                that.progress = 1;
                clearInterval(that._timer);
            }

            applyProgress();
        };


        that.start = function () {
            // Запуск анимации
            if (that.paused && (that.progress < 1)) {
                that.paused = false;

                if (that.progress) {
                    that._start = $.now() - (that.progress * that.duration);
                } else {
                    that._start = $.now();
                }
                that._timer = setInterval(timerHandle, that.settings.delay);

                that.settings.start.call(that);
            }
            return that
        };

        that.stop = function (jumpToEnd) {
            // Остановка анимации
            if (!that.paused) {
                clearInterval(that._timer);
                that.paused = true;

                if (jumpToEnd) {
                    that.progress = 1;
                    applyProgress();
                } else {
                    that.settings.stop.call(that);
                }
            }
            return that
        };

        that.reset = function () {
            // Сброс анимации
            that.progress = 0;
            if (!that.paused) {
                that._start = $.now();
            }
            that.duration = Math.max(that.settings.duration || 0, 20);
            return that
        };

        // Инициализация
        that.reset();
        that.settings.init.call(that);

        if (!that.settings.paused) {
            that.start();
        }
    }

    $.animate = function (options) {
        return new Animation(options);
    };

})(jQuery);