(function($) {

    // Видео на фоне
    $(document).ready(function() {
        var $video = $('#video').winHeight();

        $video.find('.video-bg').on('loadeddata', function() {
            $video.addClass('video-loaded');
        });
    });

    $(window).on('load', function() {
        $('#video').addClass('video-loaded');
    });

    // Parallax
    $(document).ready(function() {
        $('#parallax_sample').parallax();
    });

    // Appear - блоки
    $(document).ready(function() {
        $('.appear-block').appear({
            from_top: 1,
            from_bottom: 1
        }).on('appear', function() {
            $(this).addClass('visible');
        });
    });

    // Slider
    $(document).ready(function() {
        var $elem = $('.slider');

        window.slider = new Slider($elem, {
            adaptiveHeight: true,
            adaptiveHeightTransition: 800,
            slideItems: 2
        }).attachPlugin(
            new SliderControlsPlugin()
        ).attachPlugin(
            new SliderNavigationPlugin()
        ).attachPlugin(
            new SliderAutoscrollPlugin({
                direction: 'random',
                animated: false
            })
        ).attachPlugin(
            new SliderSideAnimation({
                speed: 800
            })
        );
    });

})(jQuery);
