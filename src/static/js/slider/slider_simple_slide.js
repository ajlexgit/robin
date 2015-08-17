(function($) {

    window.SliderSimpleAnimationPlugin = (function(parent) {
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

                var diff = toIndex - fromIndex;
                var right_way = diff + (diff > 0 ? 0 : slides_count);
                var left_way = (diff > 0 ? slides_count : 0) - diff;

                if (right_way < left_way) {
                    this.slideRight(slider, $fromSlide, $toSlide);
                } else {
                    this.slideLeft(slider, $fromSlide, $toSlide);
                }
            } else {
                if (toIndex > fromIndex) {
                    this.slideRight(slider, $fromSlide, $toSlide);
                } else {
                    this.slideLeft(slider, $fromSlide, $toSlide);
                }
            }
        };

        SliderSimpleAnimationPlugin.prototype.slideRight = function(slider, $fromSlide, $toSlide) {
            if ($fromSlide._animation) {
                return
            }

            $fromSlide.css({
                zIndex: 5
            });
            $toSlide.css({
                left: '100%',
                zIndex: 10
            });

            slider.$currentSlide = $toSlide;

            $fromSlide._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.initial = parseInt($fromSlide.get(0).style.left);
                    this.diff = -100 - this.initial;
                },
                step: function(eProgress) {
                    $fromSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $fromSlide._animation = null;
                }
            });

            $toSlide._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.initial = parseInt($toSlide.get(0).style.left);
                    this.diff = -this.initial;
                },
                step: function(eProgress) {
                    $toSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $toSlide._animation = null;
                }
            });
        };

        SliderSimpleAnimationPlugin.prototype.slideLeft = function(slider, $fromSlide, $toSlide) {
            if ($fromSlide._animation) {
                return
            }

            $fromSlide.css({
                zIndex: 5
            });
            $toSlide.css({
                left: '-100%',
                zIndex: 10
            });

            slider.$currentSlide = $toSlide;

            $fromSlide._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.initial = parseInt($fromSlide.get(0).style.left);
                    this.diff = 100 - this.initial;
                },
                step: function(eProgress) {
                    $fromSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $fromSlide._animation = null;
                }
            });

            $toSlide._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.initial = parseInt($toSlide.get(0).style.left);
                    this.diff = -this.initial;
                },
                step: function(eProgress) {
                    $toSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $toSlide._animation = null;
                }
            });
        };

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
