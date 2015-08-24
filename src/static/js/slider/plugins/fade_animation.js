(function($) {

    window.SliderFadeAnimation = (function(parent) {
        var defaults = {
            name: 'fade',
            speed: 800,
            easing: 'linear'
        };

        // Инициализация плагина
        var FadeAnimation = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = FadeAnimation; };
        _.prototype = parent.prototype;
        FadeAnimation.prototype = new _;

        /*
            Реализация метода перехода от одного слайда к другому
            посредством исчезания
         */
        FadeAnimation.prototype.slideTo = function(slider, $toSlide, animatedHeight) {
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
            slider._setCurrentSlide($toSlide);
            slider.updateListHeight(animatedHeight);

            slider._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                step: function(eProgress) {
                    $fromSlide.css({
                        opacity: 1 - eProgress
                    });
                    $toSlide.css({
                        opacity: eProgress
                    });
                }, complete: function() {
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
        };

        return FadeAnimation;
    })(SliderPlugin);

})(jQuery);
