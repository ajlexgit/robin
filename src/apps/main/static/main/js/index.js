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
        $appear_block = $('.appear-block');
        $appear_block.appear().on('appear', function() {
            $appear_block.addClass('visible');
        });
    });

    // Slider
    $(document).ready(function() {
        $('#slider_example').find('.slider3d').slider3d({

        });
    });

})(jQuery);