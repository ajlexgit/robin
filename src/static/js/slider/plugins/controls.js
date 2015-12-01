(function($) {

    window.SliderControlsPlugin = Class(SliderPlugin, function(cls, superclass) {
        cls.init = function(settings) {
            var result = superclass.init.call(this, settings);
            if (result === false) {
                return false
            }

            if (!this.opts.animationName) {
                console.error('Controls plugin must set animationName');
                return false;
            }
        };

        // Настройки по умолчанию
        cls.prototype.getDefaultOpts = function() {
            return $.extend(superclass.prototype.getDefaultOpts.call(this), {
                animationName: '',
                animatedHeight: true,

                arrowClass: 'slider-arrow',
                arrowLeftClass: 'slider-arrow-left',
                arrowRightClass: 'slider-arrow-right',
                arrowDisabledClass: 'slider-arrow-disabled',

                container: null,
                disableOnEnd: true
            });
        };

        /*
            Создание стрелок при подключении плагина
         */
        cls.prototype.onAttach = function(slider) {
            superclass.prototype.onAttach.call(this, slider);

            this.createControls(slider);
            this.checkAllowed(slider);
        };

        /*
            Деактивируем стрелки на границах сладера
         */
        cls.prototype.afterSetCurrentSlide = function(slider) {
            this.checkAllowed(slider);
        };

        /*
            Создание стрелок
         */
        cls.prototype.createControls = function(slider) {
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
        cls.prototype.createControlItems = function(slider) {
            var that = this;

            this.$left = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowLeftClass)
                .append('<span>')
                .on('click.slider.controls', function() {
                    if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                        return false
                    }

                    slider.slidePrevious(that.opts.animationName, that.opts.animatedHeight);
                });

            this.$right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
                .append('<span>')
                .on('click.slider.controls', function() {
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
        cls.prototype.checkAllowed = function(slider) {
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
