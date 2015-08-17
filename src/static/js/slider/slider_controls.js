(function($) {

    window.SliderControlsPlugin = (function(parent) {
        var defaults = {
            container: null
        };

        // Инициализация плагина
        var SliderControlsPlugin = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = SliderControlsPlugin; };
        _.prototype = parent.prototype;
        SliderControlsPlugin.prototype = new _;


        // Подключение плагина
        SliderControlsPlugin.prototype.onAttach = function(slider) {
            parent.prototype.onAttach.call(this, slider);

            // Добавление стрелок
            var $container = this.getContainer(slider);
            if ($container.length) {
                $container = $container.first();
                slider.controls = this.createControls(slider, $container);
            }

            slider.slideNext = function() {
                var $curr = this.$currentSlide;
                var $next = this.getNextSlide($curr);
                if (!$next || !$next.length) {
                    return
                }

                this.slide($curr, $next);
            };

            slider.slidePrevious = function() {
                var $curr = this.$currentSlide;
                var $prev = this.getPreviousSlide($curr);
                if (!$prev || !$prev.length) {
                    return
                }

                this.slide($curr, $prev);
            };
        };

        // Метод, возвращающий контейнер, куда будут добавлены стрелки
        SliderControlsPlugin.prototype.getContainer = function(slider) {
            if (this.opts.container) {
                var $container = $(this.opts.container);
            } else {
                $container = slider.$root
            }
            return $container;
        };

        // Метод, добавляющий стрелки
        SliderControlsPlugin.prototype.createControls = function(slider, $container) {
            var $left = $('<div>')
                .addClass('slider-arrow slider-arrow-left')
                .appendTo($container)
                .on('click', function() {
                    slider.slidePrevious();
                });

            var $right = $('<div>')
                .addClass('slider-arrow slider-arrow-right')
                .appendTo($container)
                .on('click', function() {
                    slider.slideNext();
                });

            return {
                left: $left,
                right: $right
            };
        };

        return SliderControlsPlugin;
    })(SliderPlugin);

})(jQuery);
