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
        $('#sticky_example').find('.yellow').sticky({
            topOffset: 50,
            bottomOffset: 50
        });
    });

    // Layer
    $(document).ready(function() {
        var $layer = $('#layer_example');
        $layer.find('.yellow').layer({
            speed: 0.2
        });
        $layer.find('.green').layer({
            speed: 0.3
        });
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
                this.addPlacemark({
                    lng: 49.418785,
                    lat: 53.510171,
                    hint: 'First',
                    balloon: '<p>Hello</p>'
                });

                this.addPlacemark({
                    lng: 49.435000,
                    lat: 53.525000,
                    hint: 'second',
                    draggable: true,
                    balloon: '<p>Goodbay</p>'
                });

                this.setCenter(this.getPoints());
            }
        });
    });

    // Yandex map
    $(document).ready(function() {
        window.ymap = YandexMap.create('.yandex-map', {
            onInit: function() {
                this.addPlacemark({
                    lng: 49.418785,
                    lat: 53.510171,
                    hint: 'First',
                    balloon: '<p>Hello</p>'
                });

                this.addPlacemark({
                    lng: 49.435000,
                    lat: 53.525000,
                    hint: 'second',
                    draggable: true,
                    balloon: '<p>Goodbay</p>'
                });

                this.setCenter(this.getPoints());
            }
        });
    });

    // slider
    $(document).ready(function() {
        var $elem = $('#slider_example').find('.slider');
        window.slider = Slider.create($elem, {
            adaptiveHeight: true,
            adaptiveHeightTransition: 800,
            itemsPerSlide: 2
        }).attachPlugins(
            [
                SliderSideAnimation.create({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                SliderSideShortestAnimation.create({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                SliderFadeAnimation.create({
                    speed: 800
                }),
                SliderControlsPlugin.create({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin.create({
                    animationName: 'side'
                }),
                SliderDragPlugin.create({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                SliderAutoscrollPlugin.create({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 3000
                })
            ]
        );
    });

    // Вкладки
    $(document).ready(function() {
        $('#tabs').tabManager();
    })

})(jQuery);
