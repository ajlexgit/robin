(function($) {

    window.SliderAutoscrollPlugin = Class(SliderPlugin, function(cls, superclass) {
        cls.init = function(settings) {
            var result = superclass.init.call(this, settings);
            if (result === false) {
                return false;
            }

            if (!this.opts.animationName) {
                console.error('Autoscroll plugin must set animationName');
                return false;
            }
        };

        // Настройки по умолчанию
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                animationName: '',
                animatedHeight: true,

                direction: 'next',  // next / prev / random
                stopOnHover: true,
                interval: 3000
            });
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.prototype.onAttach = function(slider) {
            superclass.prototype.onAttach.call(this, slider);

            if (this.opts.direction == 'prev') {
                this._timerHandler = $.proxy(
                    slider.slidePrevious,
                    slider,
                    this.opts.animationName,
                    this.opts.animatedHeight
                );
            } else if (this.opts.direction == 'random') {
                this._timerHandler = $.proxy(this.slideToRandom, this, slider);
            } else {
                this._timerHandler = $.proxy(
                    slider.slideNext,
                    slider,
                    this.opts.animationName,
                    this.opts.animatedHeight
                );
            }

            this.startTimer(slider);

            // остановка таймера при наведении на слайдер
            if (this.opts.stopOnHover) {
                var that = this;
                slider.$root.on('mouseenter.slider.autoscroll', function() {
                    that.stopTimer(slider);
                }).on('mouseleave.slider.autoscroll', function() {
                    that.startTimer(slider);
                });
            }
        };


        /*
            Переустановка таймера при измеении кол-ва слайдов
         */
        cls.prototype.afterSetItemsPerSlide = function(slider) {
            if (this._timer) {
                this.startTimer(slider);
            }
        };

        /*
            Создание таймера
         */
        cls.prototype.startTimer = function(slider) {
            if (slider.$slides.length < 2) {
                return
            }

            if (this._timer) {
                clearInterval(this._timer);
            }

            this._timer = setInterval(this._timerHandler, this.opts.interval);
        };

        /*
            Остановка таймера
         */
        cls.prototype.stopTimer = function() {
            if (this._timer) {
                clearInterval(this._timer);
                this._timer = null;
            }
        };

        /*
            Скролл на рандом
         */
        cls.prototype.slideToRandom = function(slider) {
            var slides_count = slider.$slides.length;
            var random_index = Math.floor(Math.random() * (slides_count - 1));
            var current_index = slider.$slides.index(slider.$currentSlide);
            var final_index = (random_index < current_index) ? random_index : random_index + 1;

            slider.slideTo(slider.$slides.eq(final_index), this.opts.animationName, this.opts.animatedHeight);
        };
    });

})(jQuery);
