(function($) {

    // Видео на фоне
    $(document).ready(function() {
        var $video = $('#video').winHeight();
        $video.find('.section-video').on('loadeddata', function() {
            $video.addClass('video-loaded');
        });

        // autoplay video
        if (window.innerWidth >= 1024) {
            $video.find('.section-video').attr({
                autoplay: true,
                preload: 'auto'
            });
        }
    });

    $(window).on('load', function() {
        $('#video').addClass('video-loaded');
    });


    // Sticky
    $(document).ready(function() {
        new Sticky('#sticky_example .yellow');
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


    $(document).ready(function() {
        // slider
        var $elem = $('.slider');
        window.slider = new Slider($elem, {
            adaptiveHeight: true,
            adaptiveHeightTransition: 800,
            slideItems: 2
        }).attachPlugins(
            [
                new SliderSideAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                new SliderSideShortestAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                new SliderFadeAnimation({
                    speed: 800
                }),
                new SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                new SliderNavigationPlugin({
                    animationName: 'side'
                }),
                new SliderDragPlugin({
                    speed: 800,
                    slideMarginPercent: 5
                })/*,
                new SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 3000
                })*/
            ]
        );
    });

})(jQuery);
