(function($) {

    window.SliderControlsPlugin = Class(SliderPlugin, function SliderControlsPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animatedHeight: true,

            arrowClass: 'slider-arrow',
            arrowLeftClass: 'slider-arrow-left',
            arrowRightClass: 'slider-arrow-right',
            arrowDisabledClass: 'slider-arrow-disabled',

            container: null,
            disableOnEnd: true
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
            this.createControls(slider);
            this.checkAllowed(slider);
        };

        /*
            Деактивируем стрелки на границах сладера
         */
        cls.afterSetCurrentSlide = function(slider) {
            this.checkAllowed(slider);
        };

        /*
            Создание стрелок
         */
        cls.createControls = function(slider) {
            if (this.opts.container) {
                this.$container = slider.$root.find(this.opts.container).first();
            } else {
                this.$container = slider.$listWrapper;
            }

            if (this.$container.length) {
                this.createControlItems(slider);
            } else {
                this.$container = null;
            }
        };

        /*
            Добавление стрелок в DOM
         */
        cls.createControlItems = function(slider) {
            var that = this;

            this.$left = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowLeftClass)
                .append('<span>')
                .on(touchClick + '.slider.controls', function() {
                    if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                        return false
                    }

                    slider.slidePrevious(that.opts.animationName, that.opts.animatedHeight);
                });

            this.$right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
                .append('<span>')
                .on(touchClick + '.slider.controls', function() {
                    if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                        return false
                    }

                    slider.slideNext(that.opts.animationName, that.opts.animatedHeight);
                });

            this.$container.append(this.$left, this.$right);
        };

        /*
            Проверка и деактивация кнопок на границах
         */
        cls.checkAllowed = function(slider) {
            var $curr = slider.$currentSlide;
            var $next = slider.getNextSlide($curr);
            var $prev = slider.getPreviousSlide($curr);

            if (this.opts.disableOnEnd && (!$prev || !$prev.length || ($curr.get(0) == $prev.get(0)))) {
                this.$left.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$left.removeClass(this.opts.arrowDisabledClass)
            }

            if (this.opts.disableOnEnd && (!$next || !$next.length || ($curr.get(0) == $next.get(0)))) {
                this.$right.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$right.removeClass(this.opts.arrowDisabledClass)
            }
        };
    });

})(jQuery);
