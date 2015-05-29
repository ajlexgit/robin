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
                var that = this;
                $(that.element).stop();
                this.initialLeft = $(this.element).position().left;
            },
            onDrag: function(evt) {
                var that = this;
                var newLeft = that.initialLeft + evt.dx;
                $.animation_frame(function () {
                    $(that.element).css('transform', 'translateX(' + newLeft + 'px)');
                }, that.element)();
            },
            onStopDrag: function(evt) {
                var that = this;
                var startLeft = that.initialLeft + evt.dx;

                var $elem = $(that.element);
                var availWidth = $elem.parent().outerWidth() - $elem.outerWidth();

                $elem.css({
                    textIndent: startLeft
                }).animate({
                    textIndent: Math.max(0, Math.min(availWidth, startLeft + evt.momentum.dX))
                }, {
                    duration: evt.momentum.duration,
                    easing: 'easeOutCubic',
                    step: function(now) {
                        $elem.css({
                            transform: 'translateX(' + now + 'px)'
                        })
                    }
                });
            }
        });

        //$('#slider_example').find('.slider3d').slider3d();
    });

})(jQuery);