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

        var drager = new Drager($('#slider_example .front'), {
            mouse: {
                onStartDrag: function() {
                    console.log('mousedown');
                },
                onDrag: function() {
                    console.log('mousemove', this.getDx(), this.getDy(), this.speed);
                },
                onStopDrag: function() {
                    console.log('mouseup', this.getDx(), this.getDy(), this.speed);
                }
            },
            touch: {
                onStartDrag: function() {
                    console.log('touchstart');
                },
                onDrag: function() {
                    console.log('touchmove', this.getDx(), this.getDy(), this.speed);
                },
                onStopDrag: function() {
                    console.log('touchend', this.getDx(), this.getDy(), this.speed);
                }
            }
        });

        //$('#slider_example').find('.slider3d').slider3d();
    });

})(jQuery);