(function($) {

    /*
      У

      HTML:
        <div id="video" class="video-bg">
          <div class="video-bg-wrapper">
            <video preload="auto" src="{% static '../img/bay4.mp4' %}" autoplay="" loop=""></video>
          </div>
          ...
        </div>

      JS:
        $('#video').videoBackground({
          fullHeightBlock: true,
          top: 0.5,
          left: 0.5
        })
    */

    var blocks = [];

    var refresh_video = function($block, settings) {
        var $video = $block.find('video');
        var win_height = $(window).outerHeight();

        if (settings.fullHeightBlock) {
            $block.height('');
            var block_height = $block.outerHeight();
            $block.outerHeight(Math.max(block_height, win_height));
        }

        $video.css({
            height: '',
            width: '',
            marginLeft: '',
            marginTop: ''
        });
        var video_height = $video.outerHeight();
        block_height = $block.outerHeight();
        if (video_height < block_height) {
            $video.css({
                height: block_height,
                width: 'auto'
            });

            var video_width = $video.outerWidth();
            var block_width = $block.outerWidth();
            $video.css('marginLeft', Math.round((block_width - video_width) * settings.left));
        } else if (settings.top) {
            $video.css('marginTop', Math.round((block_height - video_height) * settings.top));
        }
    };


    var refresh_all_videos = function() {
        for (var i = 0, l = blocks.length; i < l; i++) {
            var $block = blocks[i];
            var settings = $block.data('video-bg-settings');

            if (settings) {
                refresh_video($block, settings);
            }
        }
    };


    $.fn.videoBackground = function(options) {
        var settings = $.extend({
            fullHeightBlock: true,
            top: 0.5,
            left: 0.5
        }, options);

        return $(this).each(function() {
            var $block = $(this);
            var $wrapper = $block.find('.video-bg-wrapper');
            var $video = $wrapper.find('video');

            $video.off('loadedmetadata.video-bg').on('loadedmetadata.video-bg', function() {
                $(this).css('visibility', '');
                refresh_video($block, settings);
            });

            refresh_video($block, settings);

            blocks.push($block.data('video-bg-settings', settings));
        });
    };


    $(window).on('resize.video-bg', $.rared(refresh_all_videos, 150));

    $(document).ready(function () {
        refresh_all_videos();
    });

})(jQuery);