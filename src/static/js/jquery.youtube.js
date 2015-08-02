(function($) {
    /*
        https://developers.google.com/youtube/iframe_api_reference?hl=ru

        Пример:
            <div id="player"></div>

            <script>
                $.youtube($('#player'), {
                    videoId: 'HZ8CZyHid3w',
                    playerVars: {
                        autoplay: 1
                    },
                }, function(player) {
                    if (player.startVideo) {
                        player.startVideo();
                    }
                })
            </script>
    */

    var script = false;
    var ready = false;

    window.onYouTubeIframeAPIReady = function() {
        ready = true;
        $(document).trigger('ready.youtube');
    };

    $.youtube = function(element, options, callback) {
        if (!script) {
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            script = true;
        }

        if (element.jquery) {
            element = element.get(0);
        }

        if (ready) {
            var player = new YT.Player(element, options);
            if ($.isFunction(callback)) {
                callback(player);
            }
        } else {
            $(document).one('ready.youtube', function() {
                var player = new YT.Player(element, options);
                if ($.isFunction(callback)) {
                    callback(player);
                }
            })
        }
    }

})(jQuery);
