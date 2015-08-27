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

                container: null
            };
        };

        /*
            Создание стрелок при подключении плагина
         */
        ControlsPlugin.prototype.onAttach = function(slider) {
            parent.prototype.onAttach.call(this, slider);

            this.createControls(slider);

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
            var $left = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowLeftClass)
                .on('click.slider.controls', function() {
                    slider.slidePrevious();
                });

            var $right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
                .on('click.slider.controls', function() {
                    slider.slideNext();
                });

            this.$container.append($left, $right);
        };

        return ControlsPlugin;
    })(SliderPlugin);

})(jQuery);
