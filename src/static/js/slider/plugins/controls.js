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
                arrowClass: 'slider-arrow',
                arrowLeftClass: 'slider-arrow-left',
                arrowRightClass: 'slider-arrow-right',

                animationName: '',
                animatedHeight: true,
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
                if (!$next || !$next.length) {
                    return
                }

                this.slideTo($next, that.opts.animationName, that.opts.animatedHeight);
            };

            slider.slidePrevious = function() {
                var $prev = this.getPreviousSlide(this.$currentSlide);
                if (!$prev || !$prev.length) {
                    return
                }

                this.slideTo($prev, that.opts.animationName, that.opts.animatedHeight);
            };
        };


        /*
            Создание стрелок
         */
        ControlsPlugin.prototype.createControls = function(slider) {
            this.$container = this.getContainer(slider);
            if (this.$container.length) {
                this.$container = this.$container.first();
                this.createControlItems(slider);
            } else {
                this.$container = null;
            }
        };

        /*
            Возвращает контейнер, в который будут добавлены стрелки
         */
        ControlsPlugin.prototype.getContainer = function(slider) {
            if (this.opts.container) {
                var $container = $(this.opts.container);
            } else {
                $container = slider.$listWrapper
            }
            return $container;
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
