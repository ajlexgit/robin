(function($) {

    window.SliderAutoscrollPlugin = (function(parent) {
        var defaults = {
            direction: 'next',  // next / prev / random
            stopOnHover: true,
            animated: true,
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
            if (this.opts.direction == 'prev') {
                this._timerHandler = $.proxy(this.slideToPrev, this, slider);
            } else if (this.opts.direction == 'random') {
                this._timerHandler = $.proxy(this.slideToRandom, this, slider);
            } else {
                this._timerHandler = $.proxy(this.slideToNext, this, slider);
            }

            // анимированный переход или нет
            if (this.opts.animated) {
                this._slideTo = $.proxy(slider.slideTo, slider);
            } else {
                this._slideTo = $.proxy(slider.slideNowTo, slider);
            }

            this.startTimer(slider);

            // остановка таймера при наведении на слайдер
            if (this.opts.stopOnHover) {
                var that = this;
                slider.$listWrapper.on('mouseenter.slider.autoscroll', function () {
                    that.stopTimer();
                }).on('mouseleave.slider.autoscroll', function () {
                    that.startTimer();
                });
            }
        };


        /*
            Создание таймера
         */
        AutoscrollPlugin.prototype.startTimer = function() {
            if (this._timer) {
                clearInterval(this._timer);
            }
            this._timer = setInterval(this._timerHandler, this.opts.interval);
        };

        /*
            Остановка таймера
         */
        AutoscrollPlugin.prototype.stopTimer = function() {
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

            this._slideTo($next);
        };

        /*
            Скролл назад
         */
        AutoscrollPlugin.prototype.slideToPrev = function(slider) {
            var $prev = slider.getPreviousSlide(slider.$currentSlide);
            if (!$prev || !$prev.length) {
                return
            }

            this._slideTo($prev);
        };

        /*
            Скролл на рандом
         */
        AutoscrollPlugin.prototype.slideToRandom = function(slider) {
            var slides_count = slider.$slides.length;
            var random_index = Math.floor(Math.random() * (slides_count - 1));
            var current_index = slider.$slides.index(slider.$currentSlide);
            var final_index = (random_index < current_index) ? random_index : random_index + 1;
            this._slideTo(slider.$slides.eq(final_index));
        };

        return AutoscrollPlugin;
    })(SliderPlugin);

})(jQuery);
