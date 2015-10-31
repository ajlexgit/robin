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

    // Google map
    $(document).ready(function() {
        window.gmap = GoogleMap.create('.google-map', {
            onInit: function() {
                gmap.points = [
                    gmap.createPoint(49.418785, 53.510171),
                    gmap.createPoint(49.435000, 53.525000)
                ];

                gmap.markers = [];
                for (var i = 0, l = gmap.points.length; i < l; i++) {
                    gmap.markers.push(gmap.createMarker(gmap.points[i]));
                }

                gmap.setCenter(gmap.points);

                var bubble = gmap.createBubble('<p>Hello</p>');
                gmap.addListener(gmap.markers[0], 'click', function() {
                    bubble.open(this.map, gmap.markers[0]);
                });
            }
        });
    });

    // Yandex map
    $(document).ready(function() {
        window.ymap = YandexMap.create('.yandex-map', {
            onInit: function() {
                ymap.points = [
                    ymap.createPoint(49.418785, 53.510171),
                    ymap.createPoint(49.435000, 53.525000)
                ];

                ymap.markers = [];
                for (var i = 0, l = ymap.points.length; i < l; i++) {
                    ymap.markers.push(ymap.createMarker(ymap.points[i]));
                }

                ymap.setCenter(ymap.points);

                var bubble = ymap.createBubble('<p>Hello</p>');
                ymap.addListener(ymap.markers[0], 'click', function() {
                    bubble.open(ymap.markers[0].geometry.getCoordinates());
                });
            }
        });
    });

    // slider
    $(document).ready(function() {
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


        // вкладки
        TabManager.create('#tabs');
    });

})(jQuery);
