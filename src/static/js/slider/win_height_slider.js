(function() {
    'use strict';

    /*
        Потомок слайдера, высота которого определяется как
        минимимум из высоты окна и высоты содержимого overlay-блока.
     */

    window.WinHeightSlider = Class(Slider, function WinHeightSlider(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            sliderHeight: cls.HEIGHT_MAX,
            sliderHeightTransition: 0
        });

        cls.calcListHeight = function() {
            var overlayHeight = this.$list.find('.overlay').outerHeight();
            overlayHeight += this.$list.outerHeight() - this.$list.height();
            return Math.max(overlayHeight, document.documentElement.clientHeight);
        };
    });

})(jQuery);
