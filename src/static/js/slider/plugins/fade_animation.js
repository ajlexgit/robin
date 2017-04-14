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

            slider.$slides.attr('style', '');
            var $fromSlide = slider.$currentSlide.css({
                opacity: 1,
                zIndex: 5,
                transform: 'none'
            });
            $toSlide.css({
                opacity: 0,
                zIndex: 6,
                transform: 'none'
            });

            slider._setCurrentSlide($toSlide);


            var that = this;
            $.animation_frame(function() {
                $fromSlide.css({
                    opacity: 0,
                    transition: 'opacity ' + (that.opts.speed / 2) + 'ms ' + that.opts.easing + ' ' + (that.opts.speed / 2) + 'ms'
                });

                $toSlide.css({
                    opacity: 1,
                    transition: 'opacity ' + that.opts.speed + 'ms ' + that.opts.easing
                }).one('transitionend.slider', function() {
                    $fromSlide.css({
                        opacity: '',
                        zIndex: '',
                        transform: '',
                        transition: ''
                    });

                    $toSlide.css({
                        opacity: '',
                        zIndex: '',
                        transition: ''
                    });

                    slider.afterSlide($toSlide);
                })
            })();

            slider.softUpdateListHeight(animatedHeight);
        };
    });

})(jQuery);
