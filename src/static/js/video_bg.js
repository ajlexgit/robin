(function($) {

    /*
        Плагин для показа видео на фоне блока.
        Блок ДОЛЖЕН имень position, отличный от static.

        Тэги для отображения видео добавляются автоматически, если они не найдены.
        Есть возможность вставить тэги на страницу изначально.

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
            });

        Пример тэгов на странице:
            <div class="video-bg-wrapper">
                <video src="{% static 'main/img/river.mp4' %}" autoplay="" loop="" preload="auto"></video>
            </div>
    */

    // Позиционирование видео
    var video_position = function ($video, settings) {
        var video_width = $video.prop('videoWidth');
        var video_height = $video.prop('videoHeight');
        if (!video_width || !video_height) {
            return
        }
        var video_aspect = video_width / video_height;
        
        var $wrapper = $video.closest('.video-bg-wrapper');
        var wrapper_width = $wrapper.width();
        var wrapper_height = $wrapper.height();
        var wrapper_aspect = wrapper_width / wrapper_height;

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
        });
    }, 50));

    $.fn.videoBackground = function (options) {
        var settings = $.extend({
            left_offset: 0.5,
            top_offset: 0.5,
            onShow: $.noop
        }, options);

        return $(this).each(function () {
            var $block = $(this);

            var $wrapper = $block.find('.video-bg-wrapper');
            if (!$wrapper.length) {
                $wrapper = $('<div>').addClass('video-bg-wrapper');
                $block.prepend($wrapper);
            }

            var $video = $wrapper.find('video');
            if (!$video.length) {
                var src = $block.data('video');
                if (!src) {
                    return;
                }

                $video = $('<video>').attr({
                    src: src,
                    autoplay: '',
                    loop: '',
                    preload: 'auto'
                });
                $wrapper.prepend($video);
            }

            $video.data({
                videoBgSettings: settings
            }).on('loadeddata', function() {
                video_position($(this), settings);

                // Callback
                settings.onShow.call(this);
            });

            // Позиционируем при старте
            video_position($video, settings);
        });
    };

})(jQuery);