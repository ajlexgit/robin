(function() {

    /*

        Параллакс-эффект для блока с background-image

    */

    var parallax = function () {
        var $window = $(window);
        var win_scroll = $window.scrollTop();

        $('.parallax').each(function() {
            var $self = $(this);

            var start_point = $self.offset().top;
            var offset = win_scroll - start_point;

            $self.css({
                backgroundPosition: 'center ' + (-offset * 0.2) + 'px'
            });
        });
    };

    $(document).ready(function() {
        parallax();
    });

    $(window).on('load', function() {
        parallax();
    }).on('scroll', $.rared(parallax, 10));

})(jQuery);