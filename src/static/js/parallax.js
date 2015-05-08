(function() {

    /*

        Параллакс-эффект для блока с background-image

    */

    var parallax = function () {
        var $window = $(window);
        var win_scroll = $window.scrollTop();
        $('.parallax').each(function () {
            var $self = $(this);

            var start_point = $self.offset().top;
            var offset = win_scroll - start_point;

            var coords = 'center ' + (-offset * 0.2) + 'px';
            $self.css({backgroundPosition: coords});
        });
    };

    $(document).ready(function () {
        parallax();
    });

    $(window).on('load', function () {
        parallax();
    }).on('scroll', function () {
        parallax();
    });

})(jQuery);