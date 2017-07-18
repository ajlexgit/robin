(function($) {
    'use strict';

    window.SliderAutoscrollPlugin = Class(SliderPlugin, function SliderAutoscrollPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animateListHeight: true,

            progress_interval: 40,
            interval: 3000,
            direction: 'next',          // next / prev / random
            stopOnHover: true,

            onProgress: function(progress) {

            },
            checkEnabled: function() {
                return this.slider.$slides.length >= 2;
            }
        });

        cls.init = function(settings) {
            superclass.init.call(this, settings);
            if (!this.opts.animationName) {
                return this.raise('animationName required');
            }
        };

        cls.enable = function() {
            this.startTimer();
            superclass.enable.call(this);
        };

        cls.disable = function() {
            this.stopTimer();
            superclass.disable.call(this);
        };

        cls.destroy = function() {
            this.stopTimer();
            superclass.destroy.call(this);
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);

            if (this.opts.direction === 'prev') {
                this._timerHandler = $.proxy(
                    this.slider.slidePrevious,
                    this.slider,
                    this.opts.animationName,
                    this.opts.animateListHeight
                );
            } else if (this.opts.direction === 'next') {
                this._timerHandler = $.proxy(
                    this.slider.slideNext,
                    this.slider,
                    this.opts.animationName,
                    this.opts.animateListHeight
                );
            } else if (this.opts.direction === 'random') {
                this._timerHandler = $.proxy(
                    this.slider.slideRandom,
                    this.slider,
                    this.opts.animationName,
                    this.opts.animateListHeight
                );
            } else {
                this.error('Invalid direction: ' + this.opts.direction);
                return
            }

            this._total_steps = Math.ceil(this.opts.interval / this.opts.progress_interval);
            this._steps_done = 0;
            this._updateEnabledState();

            // остановка таймера при наведении на слайдер
            if (this.opts.stopOnHover) {
                var that = this;
                this.slider.$root.on('mouseenter.slider.autoscroll', function() {
                    that.stopTimer();
                }).on('mouseleave.slider.autoscroll', function() {
                    that.startTimer();
                });
            }
        };

        /*
            Сброс таймера при изменении кол-ва слайдов
         */
        cls.afterSetItemsPerSlide = function() {
            this.resetTimer();
        };

        /*
            Сброс таймера при переключении слайда
         */
        cls.beforeSlide = function() {
            this.resetTimer();
        };

        /*
            Переустановка таймера при перетаскивании
         */
        cls.startDrag = function() {
            this.stopTimer();
        };

        /*
            Переустановка таймера при перетаскивании
         */
        cls.stopDrag = function() {
            this._updateEnabledState();
        };

        /*
            Создание таймера
         */
        cls.startTimer = function() {
            if (!this.enabled) return;
            this.stopTimer();

            // инициализация
            this.opts.onProgress(this._steps_done / this._total_steps);

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
            if (this._timer) {
                clearInterval(this._timer);
                this._timer = null;
            }
        };

        /*
            Сброс таймера
         */
        cls.resetTimer = function() {
            this.disable();
            this._steps_done = 0;
            this._updateEnabledState();
        };
    });

})(jQuery);
