(function($) {

    /*
        Плагин для показа видео на фоне блока.
        Блок должен иметь position, отличный от static и overflow: hidden.

        Тэги для отображения видео добавляются автоматически, если они не найдены.
        Есть возможность вставить тэги на страницу изначально.

        Требует:
            rared.js

        Параметры:
            left_offset - Процентное смещение видео по горизонтали,
                          когда видео шире, чем блок. От 0 до 1.
                          По умолчанию - 0.5, что означает центр видео.

            top_offset -  Процентное смещение видео по вертикали,
                          когда видео выше, чем блок. От 0 до 1.
                          По умолчанию - 0.5, что означает центр видео.

            onShow -      Коллбэк при показе видео.

        Пример:
            <div id="block" data-video-bg="/static/main/img/video.mp4"></div>

        Пример блока с изначальной разметкой:
            <div id="block" class="video-bg-container">
                <video class="video-bg" src="{% static 'main/img/river.mp4' %}" autoplay="" loop="" preload="auto"></video>
                ...
            </div>

        JS:
            $('#block').videoBackground({
                left_offset: 0,
                top_offset: 1,
                onShow: function() {
                    console.log('video showen!');
                }
            });
    */

    // Позиционирование видео
    var video_position = function ($video, settings) {
        var video_width = $video.prop('videoWidth');
        var video_height = $video.prop('videoHeight');
        if (!video_width || !video_height) {
            return
        }
        var video_aspect = video_width / video_height;

        var $container = $video.closest('.video-bg-container');
        var container_width = $container.outerWidth();
        var container_height = $container.outerHeight();
        var container_aspect = container_width / container_height;

        if (video_aspect > container_aspect) {
            // Видео шире
            var final_video_width = Math.round((container_height * video_width) / video_height);
            $video.css({
                height: '100%',
                width: 'auto',
                left: (container_width - final_video_width) * settings.left_offset,
                top: 0
            });
        } else {
            // Видео выше
            var final_video_height = Math.round((container_width * video_height) / video_width);
            $video.css({
                height: 'auto',
                width: '100%',
                left: 0,
                top: (container_height - final_video_height) * settings.top_offset
            });
        }
    };


    // Позиционирование видео при изменении размера окна
    $(window).on('resize.videoBackground', $.rared(function() {
        $('.video-bg-container > .video-bg:first').each(function() {
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
            var $block = $(this).addClass('video-bg-container');

            var $video = $block.children('.video-bg:first');
            if (!$video.length) {
                var src = $block.data('video-bg');
                if (!src) {
                    return;
                }

                $video = $('<video>').attr({
                    src: src,
                    autoplay: '',
                    loop: '',
                    preload: 'auto'
                });
                $block.prepend($video);
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