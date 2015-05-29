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

        var drager = new Drager($('#slider_example').find('.handler'), {
            onStartDrag: function(evt) {
                var $target = $(evt.target);

                $target.stop();
                this.initialLeft = $target.position().left;
            },
            onDrag: function(evt) {
                var $target = $(evt.target);
                var newLeft = this.initialLeft + evt.dx;

                $.animation_frame(function() {
                    $target.css('transform', 'translateX(' + newLeft + 'px)');
                }, evt.target)();
            },
            onStopDrag: function(evt) {
                var $target = $(evt.target);
                var startLeft = this.initialLeft + evt.dx;
                var availWidth = $target.parent().outerWidth() - $target.outerWidth();

                $target.css({
                    textIndent: startLeft
                }).animate({
                    textIndent: Math.max(0, Math.min(availWidth, startLeft + evt.momentum.dX))
                }, {
                    duration: evt.momentum.duration,
                    easing: 'easeOutCubic',
                    step: function(now) {
                        $target.css({
                            transform: 'translateX(' + now + 'px)'
                        })
                    }
                });
            }
        });

        //$('#slider_example').find('.slider3d').slider3d();
    });

})(jQuery);