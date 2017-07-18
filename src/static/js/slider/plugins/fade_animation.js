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
        cls.slideTo = function($toSlide, animateListHeight) {
            this.slider.stopAnimation(true);
            this.slider._beforeSlide($toSlide);

            var $fromSlide = this.slider.$currentSlide.stop(true, false).css({
                zIndex: 6
            });
            $toSlide.stop(true, true).css({
                transform: 'none',
                opacity: 0,
                zIndex: 7
            });

            this.slider._setCurrentSlide($toSlide);

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

            var that = this;
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

                    that.slider._afterSlide($toSlide);
                }
            });

            this.slider.softUpdateListHeight(animateListHeight);
        };
    });

})(jQuery);
