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
            new SliderControlsPlugin({
                animationName: 'side'
            })
        ).attachPlugin(
            new SliderNavigationPlugin({
                animationName: 'side'
            })
        ).attachPlugin(
            new SliderAutoscrollPlugin({
                direction: 'random',
                interval: 3000,
                animationName: 'fade'
            })
        ).attachPlugin(
            new SliderSideAnimation({
                slideMarginPercent:5
            })
        ).attachPlugin(
            new SliderFadeAnimation()
        );
    });

})(jQuery);
