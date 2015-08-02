(function($) {

    /*
        https://developer.vimeo.com/player/js-api

        Пример:
            <div id="player"></div>

            <script>
                $.vimeo($('#player'), {
                    videoId: '116908919',
                    autoplay: true
                }, function(player) {
                    if (player.api) {
                        player.api('play');
                    }
                })
            </script>
    */

    var script = false;
    var ready = false;

    window.onVimeoAPIReady = function() {
        ready = true;
        $(document).trigger('ready.vimeo');
    };

    $.vimeo = function(element, options, callback) {
        if (!script) {
            var tag = document.createElement('script');
            tag.onload = onVimeoAPIReady;
            tag.src = "https://f.vimeocdn.com/js/froogaloop2.min.js";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            script = true;
        }

        if (typeof element == 'string') {
            element = $('#' + element)
        } else if (!element.jquery) {
            element = $(element)
        }

        var params = '';
        if (options.autoplay) {
            params = '&autoplay=1';
        }

        var $frame = $('<iframe>').attr({
            id: element.attr('id'),
            src: ('//player.vimeo.com/video/%s?api=1' + params).replace('%s', options.videoId),
            frameborder: '0',
            webkitallowfullscreen: '',
            mozallowfullscreen: '',
            allowfullscreen: ''
        });
        element.replaceWith($frame);

        if (ready) {
            if ($.isFunction(callback)) {
                callback($f($frame.get(0)));
            }
        } else {
            $(document).one('ready.vimeo', function() {
                if ($.isFunction(callback)) {
                    callback($f($frame.get(0)));
                }
            })
        }
    }

})(jQuery);
