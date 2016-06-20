(function($) {
    'use strict';

    /*
        Загрузчик асинхронных блоков.

        Требует:
            jquery.utils.js

        Для отлова события загрузки всех блоков можно
        использовать событие "ready.ajax_blocks":
            $(document).on('ready.ajax_blocks', function() {

            })
     */

    $(document).ready(function() {
        // собираем все ключи кэшированных блоков
        var keys = [];
        var $blocks = $('.async-block');
        $blocks.each(function() {
            var key = $(this).data('id');
            if (key) {
                keys.push(key);
            }
        });

        if (!keys.length) return;
        $.ajax({
            url: window.js_storage.ajax_attached_block,
            type: 'POST',
            data: {
                keys: keys
            },
            dataType: 'json',
            success: function(response) {
                $blocks.each(function() {
                    var $this = $(this);
                    var key = $this.data('id');
                    if (!key || !(key in response)) {
                        $this.remove();
                        return
                    }

                    $this.replaceWith(response[key]);
                });

                // callback event
                $(document).trigger('ready.ajax_blocks');
            }
        });
    });

})(jQuery);
