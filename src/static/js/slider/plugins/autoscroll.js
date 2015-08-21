(function($) {

    window.SliderAutoscrollPlugin = (function(parent) {
        var defaults = {
            next: true,
            stopOnHover: true,
            interval: 3000
        };

        // Инициализация плагина
        var AutoscrollPlugin = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = AutoscrollPlugin; };
        _.prototype = parent.prototype;
        AutoscrollPlugin.prototype = new _;


        /*
            Создание кнопок при подключении плагина
         */
        AutoscrollPlugin.prototype.onAttach = function(slider) {
            if (this.opts.next) {
                this._timerHandler = $.proxy(this.slideToNext, this, slider);
            } else {
                this._timerHandler = $.proxy(this.slideToPrev, this, slider);
            }

            this.startTimer(slider);

            // остановка таймера при наведении на слайдер
            if (this.opts.stopOnHover) {
                var that = this;
                slider.$listWrapper.on('mouseenter.slider.autoscroll', function () {
                    that.stopTimer(slider);
                }).on('mouseleave.slider.autoscroll', function () {
                    that.startTimer(slider);
                });
            }
        };


        /*
            Создание таймера
         */
        AutoscrollPlugin.prototype.startTimer = function(slider) {
            this._timer = setInterval(this._timerHandler, this.opts.interval);
        };

        /*
            Остановка таймера
         */
        AutoscrollPlugin.prototype.stopTimer = function(slider) {
            if (this._timer) {
                clearInterval(this._timer);
                this._timer = null;
            }
        };

        /*
            Скролл вперед
         */
        AutoscrollPlugin.prototype.slideToNext = function(slider) {
            var $next = slider.getNextSlide(slider.$currentSlide);
            if (!$next || !$next.length) {
                return
            }

            slider.slideTo($next);
        };

        /*
            Скролл назад
         */
        AutoscrollPlugin.prototype.slideToPrev = function(slider) {
            var $prev = slider.getPreviousSlide(slider.$currentSlide);
            if (!$prev || !$prev.length) {
                return
            }

            slider.slideTo($prev);
        };

        return AutoscrollPlugin;
    })(SliderPlugin);

})(jQuery);
