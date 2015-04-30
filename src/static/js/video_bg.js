(function($) {

    /*
        Плагин для показа видео на фоне блока.
        Блок ДОЛЖЕН имень position, отличный от static.

        Параметры:
            left_offset - Процентное смещение видео по горизонтали,
                          когда видео шире, чем блок. От 0 до 1.
                          По умолчанию - 0.5, что означает центр видео.

            top_offset -  Процентное смещение видео по вертикали,
                          когда видео выше, чем блок. От 0 до 1.
                          По умолчанию - 0.5, что означает центр видео.

            onShow -      Коллбэк при показе видео.

        Пример:
            <div id="block" data-video="/static/main/img/video.mp4"></div>

            // Всегда будет виден нижний левый угол видео
            $('#block').videoBackground({
                left_offset: 0,
                top_offset: 1,
                onShow: function() {
                    console.log('video showen!');
                }
            })
    */

    // Позиционирование видео
    var video_position = function ($video, settings) {
        var $wrapper = $video.closest('.video-bg-wrapper');

        var wrapper_width = $wrapper.width();
        var wrapper_height = $wrapper.height();
        var wrapper_aspect = wrapper_width / wrapper_height;
        var video_width = $video.prop('videoWidth');
        var video_height = $video.prop('videoHeight');
        var video_aspect = video_width / video_height;

        if (video_aspect > wrapper_aspect) {
            // Видео шире
            var final_video_width = Math.round((wrapper_height * video_width) / video_height);
            $video.css({
                height: '100%',
                width: 'auto',
                left: (wrapper_width - final_video_width) * settings.left_offset,
                top: 0
            });
        } else {
            // Видео выше
            var final_video_height = Math.round((wrapper_width * video_height) / video_width);
            $video.css({
                height: 'auto',
                width: '100%',
                left: 0,
                top: (wrapper_height - final_video_height) * settings.top_offset
            });
        }
    };


    // Позиционирование видео при изменении размера окна
    $(window).on('resize.videoBackground', $.rared(function() {
        $('.video-bg-wrapper > video').each(function() {
            var $video = $(this);
            var settings = $video.data('videoBgSettings');
            video_position($video, settings);
        })
    }, 50));


    $.fn.videoBackground = function (options) {
        var settings = $.extend({
            left_offset: 0.5,
            top_offset: 0.5,
            onShow: $.noop
        }, options);

        return $(this).each(function () {
            var $block = $(this);

            var src = $block.data('video');
            if (!src) {
                return;
            };

            var $wrapper = $('<div>').addClass('video-bg-wrapper').css({
                position: 'absolute',
                overflow: 'hidden',
                left: 0,
                top: 0,
                width: '100%',
                height: '100%',
                zIndex: 1
            });

            var $video = $('<video>').attr({
                src: src,
                autoplay: '',
                loop: '',
                preload: 'auto',
            }).css({
                position: 'relative',
                visibility: 'hidden',
                zIndex: 1
            }).data({
                videoBgSettings: settings
            }).on('canplay', function() {
                // Показваем тэг, когда готовы к воспроизведению
                var $video = $(this).css({
                    visibility: ''
                });

                video_position($video, settings);

                // Callback
                settings.onShow.call(this);
            });

            $block.prepend($wrapper);
            $wrapper.prepend($video);
        });
    };

})(jQuery);