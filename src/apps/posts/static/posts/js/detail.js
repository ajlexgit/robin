(function($) {

    $(document).ready(function() {
        /*
            Слайдер картинок в тексте

            http://bxslider.com/options
        */
        $('.multi-image').each(function() {
            var self = $(this);
            var slider = self.bxSlider({
                slideSelector: 'img',
                onSliderLoad: function() {
                    self.removeClass('multi-image');
                }
            });

            self.on('click', 'img', function () {
                // Клик на картинках скроллит вправо
                slider.goToNextSlide();
                return false;
            });
        });
    })

})(jQuery);