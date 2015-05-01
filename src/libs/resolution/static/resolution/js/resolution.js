(function($) {

    /*
        Определение разрешения экрана и сохранение этой информации в куки.
        Требуется: jquery.cookie.js, rared.js
    */

    // Рассчет разрешения по размеру экрана
    var calcResolution = function() {
        for (var code in window.js_storage.resolutions) {
            var sizes = window.js_storage.resolutions[code];
            if (window.innerWidth >= sizes[0] && (!sizes[1] || window.innerWidth <= sizes[1])) {
                return code;
            }
        }
    };

    // Установка разрешения в куку и js_storage
    var setResolution = function() {
        var old_resolution = $.cookie('resolution'),
            resolution = calcResolution();
        if (old_resolution == resolution) {
            return;
        }

        $.cookie('resolution', resolution, {
            domain: '.' + location.host.split('.').splice(-2, 2).join('.'),
            expires: 7,
            path: '/'
        });
        window.js_storage.resolution = parseInt(resolution) || null;

        // Callback
        $(document).trigger('change_resolution', old_resolution);
    };

    // Обновление куки при изменении размера окна
    $(window).on('resize', $.rared(function() {
        setResolution();
    }, 100));

    // Если нет куки при первом заходе - ставим её
    $(document).ready(function() {
        var current_resolution = $.cookie('resolution');
        if ((current_resolution == undefined) || (current_resolution != calcResolution())) {
            setResolution();
        }
    });

})(jQuery);
