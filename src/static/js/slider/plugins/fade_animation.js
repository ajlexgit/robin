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
                return
            }

            slider.beforeSlide($toSlide);

            var $fromSlide = slider.$currentSlide.css({
                left: '0',
                zIndex: 7
            });
            $toSlide.css({
                left: '0',
                opacity: 0,
                zIndex: 6
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
                        left: '',
                        opacity: ''
                    });
                    $toSlide.css({
                        zIndex: '',
                        opacity: ''
                    });

                    slider.afterSlide($toSlide);
                }
            });

            slider.updateListHeight(animatedHeight);
        };
    });

})(jQuery);
