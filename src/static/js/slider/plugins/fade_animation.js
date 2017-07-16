(function($) {
    'use strict';

    window.SliderFadeAnimation = Class(SliderPlugin, function SliderFadeAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'fade',

            speed: 800,
            easing: 'linear'
        });

        /*
            Реализация метода перехода от одного слайда к другому
            посредством исчезания
         */
        cls.slideTo = function(slider, $toSlide, animatedHeight) {
            if (slider._animation) {
                slider._animation.stop(true, true);
                slider._animation = null;
            }

            slider.beforeSlide($toSlide);

            var $fromSlide = slider.$currentSlide.stop(true, false).css({
                zIndex: 6
            });
            $toSlide.stop(true, true).css({
                transform: 'none',
                opacity: 0,
                zIndex: 7
            });

            slider._setCurrentSlide($toSlide);

            // анимация
            $fromSlide.animate({
                opacity: 0
            }, {
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    $(this).css({
                        transform: '',
                        zIndex: '',
                        opacity: ''
                    });
                }
            });

            $toSlide.animate({
                opacity: 1
            }, {
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    $(this).css({
                        zIndex: '',
                        opacity: ''
                    });

                    slider.afterSlide($toSlide);
                }
            });

            slider.softUpdateListHeight(animatedHeight);
        };
    });

})(jQuery);
