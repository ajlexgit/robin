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
            this.checkAllowed(slider);
        };


        /*
            Деактивируем стрелки на границах сладера
         */
        ControlsPlugin.prototype.afterSetCurrentSlide = function(slider, $slide) {
            this.checkAllowed(slider);
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

                    slider.slidePrevious(that.opts.animationName, that.opts.animatedHeight);
                });

            this.$right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
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
        ControlsPlugin.prototype.checkAllowed = function(slider) {
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

        return ControlsPlugin;
    })(SliderPlugin);

})(jQuery);
