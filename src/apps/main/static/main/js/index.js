(function($) {

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

    // Parallax
    $(document).ready(function () {
        $('#parallax_sample').parallax();
    });

    // Appear - блоки
    $(document).on('appear', '.appear-block', function () {
        $(this).addClass('visible');
    }).ready(function () {
        $('.appear-block').appear();
        $.force_appear();
    });

    // Центрирование карты гугла
    $(document).on('google-maps-ready', function() {
        google.maps.event.addDomListener(window, 'resize', $.rared(function() {
            $('.google-map').each(function () {
                var gmap = $(this).data('map');
                gmap.map.setCenter(gmap.center);
            });
        }, 300));
    });

})(jQuery);