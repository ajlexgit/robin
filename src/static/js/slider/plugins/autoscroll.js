(function($) {
    'use strict';

    window.SliderAutoscrollPlugin = Class(SliderPlugin, function SliderAutoscrollPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animatedHeight: true,

            progress_interval: 40,
            interval: 3000,
            direction: 'next',          // next / prev / random
            stopOnHover: true,

            onProgress: function(progress) {

            },
            checkEnabled: function(slider) {
                return slider.$slides.length >= 2;
            }
        });

        cls.init = function(settings) {
            superclass.init.call(this, settings);
            if (!this.opts.animationName) {
                return this.raise('animationName required');
            }
        };

        cls.destroy = function(slider) {
            this.stopTimer(slider);
            superclass.destroy.call(this);
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);

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

            this._total_steps = Math.ceil(this.opts.interval / this.opts.progress_interval);
            this._steps_done = 0;
            this.checkEnabled(slider);

            // остановка таймера при наведении на слайдер
            if (this.opts.stopOnHover) {
                var that = this;
                slider.$root.on('mouseenter.slider.autoscroll', function() {
                    that.stopTimer();
                }).on('mouseleave.slider.autoscroll', function() {
                    that.startTimer();
                });
            }
        };

        /*
            Переустановка таймера при изменении кол-ва слайдов
         */
        cls.afterSetItemsPerSlide = function(slider) {
            this.checkEnabled(slider);
        };

        /*
            Включение плагина
         */
        cls.enable = function(slider) {
            this.startTimer();
            superclass.enable.call(this, slider);
        };

        /*
            Выключение плагина
         */
        cls.disable = function(slider) {
            this.stopTimer();
            superclass.disable.call(this, slider);
        };

        /*
            Переустановка таймера при перетаскивании
         */
        cls.startDrag = function(slider) {
            this.stopTimer();
        };

        /*
            Переустановка таймера при перетаскивании
         */
        cls.stopDrag = function(slider) {
            this.checkEnabled(slider);
        };

        /*
            Создание таймера
         */
        cls.startTimer = function() {
            if (!this.enabled) return;
            this.stopTimer();

            var that = this;
            this._timer = setInterval(function() {
                that._steps_done += 1;
                if (that._steps_done >= that._total_steps) {
                    that._steps_done = 0;
                    that._timerHandler();
                }

                that.opts.onProgress(that._steps_done / that._total_steps);
            }, this.opts.progress_interval);
        };

        /*
            Остановка таймера
         */
        cls.stopTimer = function() {
            if (this._timer) clearInterval(this._timer);
        };

        /*
            Скролл на рандом
         */
        cls.slideToRandom = function(slider) {
            var slides_count = slider.$slides.length;
            var random_index = Math.floor(Math.random() * (slides_count - 1));
            var current_index = slider.$slides.index(slider.$currentSlide);
            var final_index = (random_index < current_index) ? random_index : random_index + 1;

            slider.slideTo(slider.$slides.eq(final_index), this.opts.animationName, this.opts.animatedHeight);
        };
    });

})(jQuery);
