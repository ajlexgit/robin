(function($) {
    'use strict';

    /*
        Загрузчик асинхронных блоков.

        Требует:
            jquery.utils.js

        Для отлова события загрузки всех блоков можно
        использовать событие "loaded.cacheblock":
            $(document).on('loaded.cacheblock', function() {

            })
     */

    $(document).ready(function() {
        var cacheblock_class = window.js_storage.cacheblock_class;
        if (!cacheblock_class) return;

        // собираем все ключи кэшированных блоков
        var keys = [];
        var $blocks = $('.' + cacheblock_class);
        $blocks.each(function() {
            var key = $(this).data('key');
            if (key) {
                keys.push(key);
            }
        });

        if (!keys.length) {
            // callback event
            $(document).trigger('loaded.cacheblock');
            return;
        }

        $.ajax({
            url: window.js_storage.cacheblock_url,
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
                $(document).trigger('loaded.cacheblock');
            }
        });
    });

})(jQuery);
