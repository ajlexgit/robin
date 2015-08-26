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

        // slider
        var $elem = $('.slider');
        window.slider = new Slider($elem, {
            loop: true,
            adaptiveHeight: true,
            adaptiveHeightTransition: 800,
            slideItems: 1
        }).attachPlugin(
            new SliderSideAnimation({
                speed: 800,
                slideMarginPercent: 5
            })
        ).attachPlugin(
            new SliderSideLoopAnimation({
                speed: 800,
                slideMarginPercent: 5
            })
        ).attachPlugin(
            new SliderFadeAnimation()
        ).attachPlugin(
            new SliderControlsPlugin({
                animationName: 'side-loop'
            })
        ).attachPlugin(
            new SliderNavigationPlugin({
                animationName: 'side'
            })
        )/*.attachPlugin(
            new SliderAutoscrollPlugin({
                animationName: 'fade',
                direction: 'random',
                interval: 3000
            })
        )*/;

        // inlines
        window.formset = new Formset('#form .formset', {
            prefix: 'inlines'
        })
    });

})(jQuery);
