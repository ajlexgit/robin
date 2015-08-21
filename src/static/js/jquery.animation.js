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
        function(callback) {
            window.setTimeout(callback, 1000 / 60);
        };

    $.animation_frame = function(callback, element) {
        return $.proxy(handler, window, callback, element)
    };

    $.animate = function(options) {
        return new Animation(options);
    };

    var Animation = (function() {
        var Animation = function(settings) {
            this.opts = $.extend({
                duration: 1000,
                delay: 40,
                easing: 'linear',
                paused: false,

                init: $.noop,
                step: $.noop,
                start: $.noop,
                stop: $.noop,
                complete: $.noop
            }, settings);

            this.reset();
            this.paused = true;
            this.opts.init.call(this);

            if (!this.opts.paused) {
                this.start();
            }
        };

        // Сброс анимации
        Animation.prototype.reset = function() {
            this.progress = 0;
            if (!this.paused) {
                this._startTime = $.now();
            }
            this._duration = Math.max(this.opts.duration || 0, 20);
            return this
        };

        // Запуск анимации
        Animation.prototype.start = function() {
            if (this.paused && (this.progress < 1)) {
                this.paused = false;

                if (this.progress) {
                    this._startTime = $.now() - (this.progress * this._duration);
                } else {
                    this._startTime = $.now();
                }

                var timerHandle = $.proxy(this._timerHandle, this);
                this._timer = setInterval(timerHandle, this.opts.delay);

                this.opts.start.call(this);
            }
            return this
        };

        // Остановка анимации
        Animation.prototype.stop = function(jumpToEnd) {
            if (!this.paused) {
                clearInterval(this._timer);
                this.paused = true;

                if (jumpToEnd) {
                    this.progress = 1;
                    this._applyProgress();
                } else {
                    this.opts.stop.call(this);
                }
            }
            return this
        };

        // Применение шага анимации с вычислением that.progress
        Animation.prototype._timerHandle = function() {
            this.progress = ($.now() - this._startTime) / this._duration;
            if (this.progress >= 1) {
                this.progress = 1;
                clearInterval(this._timer);
            }

            this._applyProgress();
        };

        // Применение шага анимации (для уже установленного that.progress)
        Animation.prototype._applyProgress = function() {
            var easeProgress = $.easing[this.opts.easing](this.progress);
            this.opts.step.call(this, easeProgress);

            if (this.progress === 1) {
                this.stop();
                this.opts.complete.call(this);
            }
        };

        return Animation;
    })();

})(jQuery);
