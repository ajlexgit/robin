(function($) {
    'use strict';

    /*
        Загрузчик асинхронных блоков.

        Требует:
            jquery.utils.js

        Для отлова события загрузки всех блоков можно
        использовать событие "loaded.ajaxcache":
            $(document).on('loaded.ajaxcache', function() {

            })
     */

    $(document).ready(function() {
        var ajaxcache_class = window.js_storage.ajaxcache_class;
        if (!ajaxcache_class) return;

        // собираем все ключи кэшированных блоков
        var keys = [];
        var $blocks = $('.' + ajaxcache_class);
        $blocks.each(function() {
            var key = $(this).data('key');
            if (key) {
                keys.push(key);
            }
        });

        if (!keys.length) return;
        $.ajax({
            url: window.js_storage.ajaxcache_url,
            type: 'GET',
            data: {
                keys: keys.join(',')
            },
            dataType: 'json',
            success: function(response) {
                $blocks.each(function() {
                    var $this = $(this);
                    var key = $this.data('key');
                    if (!key || !(key in response)) {
                        $this.remove();
                        return
                    }

                    $this.replaceWith(response[key]);
                });

                // callback event
                $(document).trigger('loaded.ajaxcache');
            }
        });
    });

})(jQuery);
