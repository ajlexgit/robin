(function($) {

    window.SliderSimpleAnimationPlugin = (function(parent) {
        var defaults = {
            speed: 300,
            easing: 'ease-in'
        };

        // Инициализация плагина
        var SliderSimpleAnimationPlugin = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = SliderSimpleAnimationPlugin; };
        _.prototype = parent.prototype;
        SliderSimpleAnimationPlugin.prototype = new _;


        // Переопределяем метод скролла
        SliderSimpleAnimationPlugin.prototype.slide = function(slider, $fromSlide, $toSlide) {
            var fromIndex = slider.$slides.index($fromSlide);
            var toIndex = slider.$slides.index($toSlide);

            if (fromIndex == toIndex) {
                return
            }

            // определяем направление
            if (slider.opts.loop) {
                var slides_count = slider.$slides.length;
                
                if (toIndex > fromIndex) {
                    var right_way = toIndex - fromIndex;
                    var left_way = fromIndex + slides_count - toIndex;
                } else {
                    right_way = toIndex + slides_count - fromIndex;
                    left_way = fromIndex - toIndex;
                }

            } else {
                if (toIndex > fromIndex) {
                    this.slideRight(slider, $fromSlide, $toSlide);
                } else {
                    this.slideLeft(slider, $fromSlide, $toSlide);
                }
            }

            $fromSlide.css({
                'left': ''
            });
            $toSlide.css({
                'left': '0'
            });
            slider.$currentSlide = $toSlide;
        };

        SliderSimpleAnimationPlugin.prototype.slideRight = function(slider, $fromSlide, $toSlide) {

        };

        SliderSimpleAnimationPlugin.prototype.slideLeft = function(slider, $fromSlide, $toSlide) {

        };

        // Скролл к следующему слайду
//        SliderControlsPlugin.prototype.slideRight = function(slider) {
//            var $curr = slider.$currentSlide;
//            var $next = slider.getNextSlide($curr);
//            if (!$next || !$next.length) {
//                return
//            }
//
//            // можно ли крутить
//            if (this.canSlideRight(slider, $curr, $next) === false) {
//                return
//            }
//
//            this.processSlideRight(slider, $curr, $next);
//        };
//
//
//        // Подготовка текущего слайда
//        SliderControlsPlugin.prototype.canSlideRight = function(slider, $currentSlide, $nextSlide) {
//            if ($currentSlide._animation) {
//                return false
//            }
//        };
//
//        // Подготовка текущего слайда
//        SliderControlsPlugin.prototype.processSlideRight = function(slider, $currentSlide, $nextSlide) {
//            $currentSlide.css({
//                zIndex: 5
//            });
//            $nextSlide.css({
//                left: '100%',
//                zIndex: 10
//            });
//
//            slider.$currentSlide = $nextSlide;
//
//            $currentSlide._animation = $.animate({
//                duration: this.opts.speed,
//                easing: this.opts.easing,
//                init: function() {
//                    this.initial = parseInt($currentSlide.get(0).style.left);
//                    this.diff = -100 - this.initial;
//                },
//                step: function(eProgress) {
//                    $currentSlide.css('left', this.initial + this.diff * eProgress + '%');
//                },
//                complete: function() {
//                    $currentSlide._animation = null;
//                }
//            });
//
//            $nextSlide._animation = $.animate({
//                duration: this.opts.speed,
//                easing: this.opts.easing,
//                init: function() {
//                    this.initial = parseInt($nextSlide.get(0).style.left);
//                    this.diff = -this.initial;
//                },
//                step: function(eProgress) {
//                    $nextSlide.css('left', this.initial + this.diff * eProgress + '%');
//                },
//                complete: function() {
//                    $nextSlide._animation = null;
//                }
//            });
//        };
//
//
//        // Скролл к следующему слайду
//        SliderControlsPlugin.prototype.slideLeft = function(slider) {
//            var $curr = slider.$currentSlide;
//            var $prev = slider.getPreviousSlide($curr);
//            if (!$prev || !$prev.length) {
//                return
//            }
//
//            // можно ли крутить
//            if (this.canSlideLeft(slider, $curr, $prev) === false) {
//                return
//            }
//
//            this.processSlideLeft(slider, $curr, $prev);
//        };
//
//
//        // Подготовка текущего слайда
//        SliderControlsPlugin.prototype.canSlideLeft = function(slider, $currentSlide) {
//            if ($currentSlide._animation) {
//                return false
//            }
//        };
//
//        // Подготовка текущего слайда
//        SliderControlsPlugin.prototype.processSlideLeft = function(slider, $currentSlide, $previousSlide) {
//            $currentSlide.css({
//                zIndex: 5
//            });
//            $previousSlide.css({
//                left: '-100%',
//                zIndex: 10
//            });
//
//            slider.$currentSlide = $previousSlide;
//
//            $currentSlide._animation = $.animate({
//                duration: this.opts.speed,
//                init: function() {
//                    this.initial = parseInt($currentSlide.get(0).style.left);
//                    this.diff = 100 - this.initial;
//                },
//                step: function(eProgress) {
//                    $currentSlide.css('left', this.initial + this.diff * eProgress + '%');
//                },
//                complete: function() {
//                    $currentSlide._animation = null;
//                }
//            });
//
//            $previousSlide._animation = $.animate({
//                duration: this.opts.speed,
//                init: function() {
//                    this.initial = parseInt($previousSlide.get(0).style.left);
//                    this.diff = -this.initial;
//                },
//                step: function(eProgress) {
//                    $previousSlide.css('left', this.initial + this.diff * eProgress + '%');
//                },
//                complete: function() {
//                    $previousSlide._animation = null;
//                }
//            });
//        };

        return SliderSimpleAnimationPlugin;
    })(SliderPlugin);

})(jQuery);
