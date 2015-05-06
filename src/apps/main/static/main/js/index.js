(function($) {

    $(document).on('appear', '.appear-block', function () {
        $(this).addClass('visible');
    });

    $(document).ready(function() {
        $('#video').winHeight().videoBackground({
            onShow: function() {
                $('body').addClass('video-loaded');
            }
        });

        $('.appear-block').appear();
        $.force_appear();
    });

    $(window).on('load', function() {
        $('body').addClass('video-loaded');
    });
    
})(jQuery);