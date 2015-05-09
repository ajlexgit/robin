(function($) {

    // Appear - блоки
    $(document).on('appear', '.appear-block', function () {
        $(this).addClass('visible');
    }).ready(function () {
        $('.appear-block').appear();
        $.force_appear();
    });


    // Видео на фоне
    $(document).ready(function() {
        $('#video').winHeight().videoBackground({
            onShow: function() {
                $(this).closest('.video-bg-container').addClass('video-loaded');
            }
        });
    });

    $(window).on('load', function() {
        $('#video').addClass('video-loaded');
    });

})(jQuery);