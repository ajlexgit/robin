(function() {

    /*

        Параллакс-эффект для блока с background-image

    */

    var parallax_elements = [];
    var $window = $(window);

    window.fetch_parallax_blocks = function() {
        parallax_elements = [];
        $('.parallax').each(function() {
            parallax_elements.push($(this));
        });
    };

    var parallax = function () {
        var win_scroll = $window.scrollTop();

        for (var i=0, l=parallax_elements.length; i<l; i++) {
            var $self = parallax_elements[i];
            var start_point = $self.offset().top;
            var offset = win_scroll - start_point;

            $self.css({
                backgroundPosition: 'center ' + Math.round(-offset * 0.2) + 'px'
            });
        }
    };

    $(document).ready(function() {
        fetch_parallax_blocks();
        parallax();
    });

    $(window).on('load', function() {
        parallax();
    }).on('scroll', $.rared(function() {
        window.requestAnimationFrame(parallax);
    }, 50));

})(jQuery);