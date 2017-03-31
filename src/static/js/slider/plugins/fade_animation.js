(function($) {
    'use strict';

    window.SliderFadeAnimation = Class(SliderPlugin, function SliderFadeAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'fade',

            speed: 800,
            stoppable: false,
            easing: 'linear'
        });

        /*
            Реализация метода перехода от одного слайда к другому
            посредством исчезания
         */
        cls.slideTo = function(slider, $toSlide, animatedHeight) {
            if (slider._animation) {
                if (this.opts.stoppable) {
                    slider._animation.stop(true, true);
                    slider._animation = null;
                } else {
                    return
                }
            }

            slider.beforeSlide($toSlide);

            var $fromSlide = slider.$currentSlide.css({
                zIndex: 7,
                transform: 'none'
            });
            $toSlide.css({
                opacity: 0,
                zIndex: 6,
                transform: 'none'
            });

            slider._setCurrentSlide($toSlide);

            slider._animation = $({
                from_slide: 1,
                to_slide: 0
            }).animate({
                from_slide: 0,
                to_slide: 1
            }, {
                duration: this.opts.speed,
                easing: this.opts.easing,
                progress: function() {
                    $fromSlide.css({
                        opacity: this.from_slide
                    });
                    $toSlide.css({
                        opacity: this.to_slide
                    });
                },
                complete: function() {
                    $fromSlide.css({
                        zIndex: '',
                        opacity: '',
                        transform: ''
                    });
                    $toSlide.css({
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
