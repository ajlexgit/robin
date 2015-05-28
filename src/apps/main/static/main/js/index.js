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
    $(document).ready(function () {
        $('#parallax_sample').parallax();
    });

    // Appear - блоки
    $(document).ready(function () {
        $('.appear-block').appear({
            from_top: 1,
            from_bottom: 1
        }).on('appear', function() {
            $(this).addClass('visible');
        });
    });

    // Slider
    $(document).ready(function() {

        var drager = new Drager($('#slider_example .front'), {
            mouse: {
                onStartDrag: function(e) {
                    console.log('mousedown');
                },
                onDrag: function(e, dx, dy, speed) {
                    console.log('mousemove', dx, dy, speed);
                },
                onStopDrag: function(e, dx, dy, speed) {
                    console.log('mouseup', dx, dy, speed);
                }
            }
        });

        //$('#slider_example').find('.slider3d').slider3d();
    });

})(jQuery);