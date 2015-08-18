(function($) {

    window.SideAnimation = (function(parent) {
        var defaults = {
            speed: 300,
            easing: 'easeOutCubic'
        };

        // Инициализация плагина
        var SliderSimpleAnimationPlugin = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = SliderSimpleAnimationPlugin; };
        _.prototype = parent.prototype;
        SliderSimpleAnimationPlugin.prototype = new _;


        /*
            Добавление слайдеру флага анимирования для блокировки множественного нажатия
         */
        SliderSimpleAnimationPlugin.prototype.onAttach = function(slider) {
            slider._animated = false;

            slider.$list.css('transition', 'height ' + (this.opts.speed / 1000) + 's');
        };

        SliderSimpleAnimationPlugin.prototype.beforeSlide = function(slider) {
            slider._animated = true;
        };

        SliderSimpleAnimationPlugin.prototype.afterSlide = function(slider) {
            slider._animated = false;
        };

        SliderSimpleAnimationPlugin.prototype.beforeCreateSlides = function(slider) {
            if (this._animation) {
                this._animation.stop(true)
            }
        };

        /*
            Реализация метода перехода от одного слайда к другому
            посредством выдвигания с края слайдера
         */
        SliderSimpleAnimationPlugin.prototype.slide = function(slider, $fromSlide, $toSlide) {
            if (slider._animated) {
                return
            }

            var fromIndex = slider.$slides.index($fromSlide);
            var toIndex = slider.$slides.index($toSlide);

            if (fromIndex == toIndex) {
                return
            }

            // определяем направление
            if (slider.opts.loop) {
                var slides_count = slider.$slides.length;

                var diff = toIndex - fromIndex;
                var right_way = diff + (diff > 0 ? 0 : slides_count);
                var left_way = (diff > 0 ? slides_count : 0) - diff;

                if (left_way < right_way) {
                    this.slideLeft(slider, $fromSlide, $toSlide);
                } else {
                    this.slideRight(slider, $fromSlide, $toSlide);
                }
            } else {
                if (toIndex > fromIndex) {
                    this.slideRight(slider, $fromSlide, $toSlide);
                } else {
                    this.slideLeft(slider, $fromSlide, $toSlide);
                }
            }
        };

        /*
            Появление нового слайда справа от текущего
         */
        SliderSimpleAnimationPlugin.prototype.slideRight = function(slider, $fromSlide, $toSlide) {
            slider.beforeSlide($fromSlide, $toSlide);

            $fromSlide.css({
                zIndex: 5
            });
            $toSlide.css({
                left: '100%',
                zIndex: 10
            });
            slider.setCurrentSlide($toSlide);

            this._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.from_initial = parseInt($fromSlide.get(0).style.left);
                    this.from_diff = -100 - this.from_initial;

                    this.to_initial = parseInt($toSlide.get(0).style.left);
                    this.to_diff = -this.to_initial;
                },
                step: function(eProgress) {
                    $fromSlide.css('left', this.from_initial + this.from_diff * eProgress + '%');
                    $toSlide.css('left', this.to_initial + this.to_diff * eProgress + '%');
                },
                complete: function() {
                    slider._animated = false;
                    slider.afterSlide($fromSlide, $toSlide);
                }
            });
        };

        /*
            Появление нового слайда слева от текущего
         */
        SliderSimpleAnimationPlugin.prototype.slideLeft = function(slider, $fromSlide, $toSlide) {
            slider.beforeSlide($fromSlide, $toSlide);

            $fromSlide.css({
                zIndex: 5
            });
            $toSlide.css({
                left: '-100%',
                zIndex: 10
            });
            slider.setCurrentSlide($toSlide);

            this._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.from_initial = parseInt($fromSlide.get(0).style.left);
                    this.from_diff = 100 - this.from_initial;

                    this.to_initial = parseInt($toSlide.get(0).style.left);
                    this.to_diff = -this.to_initial;
                },
                step: function(eProgress) {
                    $fromSlide.css('left', this.from_initial + this.from_diff * eProgress + '%');
                    $toSlide.css('left', this.to_initial + this.to_diff * eProgress + '%');
                },
                complete: function() {
                    slider._animated = false;
                    slider.afterSlide($fromSlide, $toSlide);
                }
            });
        };

        return SliderSimpleAnimationPlugin;
    })(SliderPlugin);

})(jQuery);
