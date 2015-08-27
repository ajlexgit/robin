(function($) {

    window.SliderControlsPlugin = (function(parent) {
        // Инициализация плагина
        var ControlsPlugin = function(settings) {
            parent.call(this, settings);

            if (!this.opts.animationName) {
                console.error('Controls plugin must set animationName');
            }
        };

        var _ = function() {
            this.constructor = ControlsPlugin;
        };
        _.prototype = parent.prototype;
        ControlsPlugin.prototype = new _;


        // Настройки по умолчанию
        ControlsPlugin.prototype.getDefaultOpts = function() {
            return {
                animationName: '',
                animatedHeight: true,

                arrowClass: 'slider-arrow',
                arrowLeftClass: 'slider-arrow-left',
                arrowRightClass: 'slider-arrow-right',
                arrowDisabledClass: 'slider-arrow-disabled',

                container: null,
                disableOnEnd: true
            };
        };

        /*
            Создание стрелок при подключении плагина
         */
        ControlsPlugin.prototype.onAttach = function(slider) {
            parent.prototype.onAttach.call(this, slider);

            this.createControls(slider);

            // проверка на активность
            if (this.opts.disableOnEnd) {
                this.checkAllowed(slider);
            }

            var that = this;
            slider.slideNext = function() {
                var $next = this.getNextSlide(this.$currentSlide);
                if ($next.length) {
                    this.slideTo($next, that.opts.animationName, that.opts.animatedHeight);
                }
            };

            slider.slidePrevious = function() {
                var $prev = this.getPreviousSlide(this.$currentSlide);
                if ($prev.length) {
                    this.slideTo($prev, that.opts.animationName, that.opts.animatedHeight);
                }
            };
        };


        /*
            Деактивируем стрелки на границах сладера
         */
        ControlsPlugin.prototype.afterSetCurrentSlide = function(slider, $slide) {
            if (this.opts.disableOnEnd) {
                this.checkAllowed(slider);
            }
        };

        /*
            Создание стрелок
         */
        ControlsPlugin.prototype.createControls = function(slider) {
            if (this.opts.container) {
                this.$container = $.findFirstElement(this.opts.container);
            } else {
                this.$container = slider.$listWrapper;
            }

            if (this.$container.length) {
                this.createControlItems(slider);
            }
        };

        /*
            Добавление стрелок в DOM
         */
        ControlsPlugin.prototype.createControlItems = function(slider) {
            var that = this;

            this.$left = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowLeftClass)
                .on('click.slider.controls', function() {
                    if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                        return false
                    }

                    slider.slidePrevious();
                });

            this.$right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
                .on('click.slider.controls', function() {
                    if ($(this).hasClass(that.opts.arrowDisabledClass)) {
                        return false
                    }

                    slider.slideNext();
                });

            this.$container.append(this.$left, this.$right);
        };

        /*
            Проверка и деактивация кнопок на границах
         */
        ControlsPlugin.prototype.checkAllowed = function(slider) {
            var $next = slider.getNextSlide(slider.$currentSlide);
            var $prev = slider.getPreviousSlide(slider.$currentSlide);

            if (!$prev || !$prev.length) {
                this.$left.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$left.removeClass(this.opts.arrowDisabledClass)
            }

            if (!$next || !$next.length) {
                this.$right.addClass(this.opts.arrowDisabledClass)
            } else {
                this.$right.removeClass(this.opts.arrowDisabledClass)
            }
        };

        return ControlsPlugin;
    })(SliderPlugin);

})(jQuery);
