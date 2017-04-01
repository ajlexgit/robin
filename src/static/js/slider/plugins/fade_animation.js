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
            slider.beforeSlide($toSlide);

            var $fromSlide = slider.$currentSlide.css({
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
                $toSlide.css({
                    opacity: 1,
                    transition: 'opacity ' + (that.opts.speed / 1000) + 's ' + that.opts.easing
                }).one('transitionend.slider', function() {
                    $fromSlide.css({
                        zIndex: '',
                        transform: ''
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
