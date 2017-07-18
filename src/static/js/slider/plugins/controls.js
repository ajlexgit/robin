(function($) {
    'use strict';

    window.SliderControlsPlugin = Class(SliderPlugin, function SliderControlsPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animateListHeight: true,

            arrowClass: 'slider-arrow',
            arrowLeftClass: 'slider-arrow-left',
            arrowRightClass: 'slider-arrow-right',
            arrowDisabledClass: 'slider-arrow-disabled',

            container: null,
            disableOnBounds: true
        });

        cls.init = function(settings) {
            superclass.init.call(this, settings);
            if (!this.opts.animationName) {
                return this.raise('animationName required');
            }
        };

        cls.destroy = function() {
            if (this.$left) {
                this.$left.remove();
                this.$left = null;
            }
            if (this.$right) {
                this.$right.remove();
                this.$right = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Создание стрелок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this.getContainer();
            this.createControls();
            this.checkBounds();
        };

        /*
            Деактивируем стрелки на границах сладера
         */
        cls.afterSetCurrentSlide = function() {
            this.checkBounds();
        };

        /*
            Проверка и деактивация кнопок на границах
         */
        cls.checkBounds = function() {
            if (!this.opts.disableOnBounds) {
                return
            }

            var $curr = this.slider.$currentSlide;
            var $prev = this.slider.getPreviousSlide($curr);
            if (!$prev || !$prev.length || ($curr.get(0) === $prev.get(0))) {
                this.$left.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$left.removeClass(this.opts.arrowDisabledClass)
            }

            var $next = this.slider.getNextSlide($curr);
            if (!$next || !$next.length || ($curr.get(0) === $next.get(0))) {
                this.$right.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$right.removeClass(this.opts.arrowDisabledClass)
            }
        };

        /*
            Получение контейнера для элементов
         */
        cls.getContainer = function() {
            if (typeof this.opts.container === 'string') {
                this.$container = this.slider.$root.find(this.opts.container);
            } else if ($.isFunction(this.opts.container)) {
                this.$container = this.opts.container.call(this);
            } else if (this.opts.container && this.opts.container.jquery) {
                this.$container = this.opts.container;
            }

            if (!this.$container || !this.$container.length) {
                this.$container = this.slider.$listWrapper;
            } else if (this.$container.length) {
                this.$container = this.$container.first();
            }
        };

        /*
            Создание стрелок
         */
        cls.createControls = function() {
            var that = this;
            this.$left = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowLeftClass)
                .append('<span>')
                .off('.controls')
                .on('click.slider.controls', function() {
                    if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                        return false
                    }

                    that.slider.slidePrevious(
                        that.opts.animationName,
                        that.opts.animateListHeight
                    );
                });

            this.$right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
                .append('<span>')
                .off('.controls')
                .on('click.slider.controls', function() {
                    if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                        return false
                    }

                    that.slider.slideNext(
                        that.opts.animationName,
                        that.opts.animateListHeight
                    );
                });

            this.$container.append(this.$left, this.$right);
        };
    });

})(jQuery);
