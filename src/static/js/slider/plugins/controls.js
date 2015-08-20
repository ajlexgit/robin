(function($) {

    window.ControlsPlugin = (function(parent) {
        var defaults = {
            arrowClass: 'slider-arrow',
            arrowLeftClass: 'slider-arrow-left',
            arrowRightClass: 'slider-arrow-right',
            container: null
        };

        // Инициализация плагина
        var ControlsPlugin = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = ControlsPlugin; };
        _.prototype = parent.prototype;
        ControlsPlugin.prototype = new _;


        /*
            Добавление методов слайдеру и добавление стрелок в DOM слайдера
         */
        ControlsPlugin.prototype.onAttach = function(slider) {
            parent.prototype.onAttach.call(this, slider);

            this.createControls(slider);

            slider.slideNext = function() {
                var $next = this.getNextSlide(this.$currentSlide);
                if (!$next || !$next.length) {
                    return
                }

                this.slide($next);
            };

            slider.slidePrevious = function() {
                var $prev = this.getPreviousSlide(this.$currentSlide);
                if (!$prev || !$prev.length) {
                    return
                }

                this.slide($prev);
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
                $container = slider.$root
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
                .on('click.slider', function() {
                    slider.slidePrevious();
                });

            var $right = $('<div>')
                .addClass(this.opts.arrowClass)
                .addClass(this.opts.arrowRightClass)
                .on('click.slider', function() {
                    slider.slideNext();
                });

            this.$container.append($left, $right);
        };

        return ControlsPlugin;
    })(SliderPlugin);

})(jQuery);
