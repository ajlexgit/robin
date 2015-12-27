(function($) {

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
            if (slider._animated) {
                return
            }

            slider.beforeSlide($toSlide);

            var $fromSlide = slider.$currentSlide.css({
                left: '0',
                zIndex: 4
            });
            $toSlide.css({
                left: '0',
                opacity: 0,
                zIndex: 3
            });
            slider.setCurrentSlide($toSlide);

            slider._animation = $.animate({
                duration: this.opts.speed,
                delay: 50,
                easing: this.opts.easing,
                init: function() {
                    this.autoInit('from_slide_opacity', 1, 0);
                    this.autoInit('to_slide_opacity', 0, 1);
                },
                step: function(eProgress) {
                    $fromSlide.css({
                        opacity: this.autoCalc('from_slide_opacity', eProgress)
                    });
                    $toSlide.css({
                        opacity: this.autoCalc('to_slide_opacity', eProgress)
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
