(function($) {

    /*
        Загрузчик асинхронных блоков.

        Требует:
            jquery.utils.js

        Ищет все элементы с классом "ajax-cache-block",
        отправляет для каждого блока AJAX-запрос на получение
        HTML-кода блока. Результат заменяет исходный элемент.
     */

    window.AjaxCacheBlock = Class(EventedObject, function AjaxCacheBlock(cls, superclass) {
        cls.defaults = {
            url: window.js_storage.ajax_cache_block,
            extraData: $.noop
        };

        cls.DATA_KEY = 'ajax-cache-block';


        cls.init = function(placeholder, options) {
            superclass.init.call(this);

            this.$placeholder = $(placeholder).first();
            if (!this.$placeholder.length) {
                return this.raise('placeholder not found');
            }

            this.opts = $.extend({}, this.defaults, options);
            if (!this.opts.url) {
                return this.raise('url is empty');
            }

            this.getBlock();

            this.$placeholder.data(this.DATA_KEY, this);
        };

        /*
            Запрос блока
         */
        cls.getBlock = function() {
            if (this._query) {
                this._query.abort();
            }

            var data = $.extend({
                key: this.$placeholder.data('key')
            }, this.opts.extraData.call(this));

            var that = this;
            return this._query = $.ajax({
                url: this.opts.url,
                type: 'GET',
                data: data,
                cache: true,
                dataType: 'json',
                success: function(response) {
                    that.ajaxSuccess(response);
                },
                error: $.parseError(function(response) {
                    that.ajaxError(response)
                })
            });
        };

        /*
            Получение ответа с разметкой блока
         */
        cls.ajaxSuccess = function(response) {
            if (response.html) {
                var $new_block = $(response.html);
                this.$placeholder.after($new_block);
                this.$placeholder.trigger('loaded', [response, $new_block]);
                this.trigger('success.ajax-cache', response, $new_block);
                this.$placeholder.remove();
            }
        };

        /*
            Ошибка получения блока
         */
        cls.ajaxError = function(response) {
            this.trigger('error.ajax-cache', response);
            this.$placeholder.remove();
        };
    });


    $(document).ready(function() {
        $('.ajax-cache-block').each(function() {
            window.AjaxCacheBlock(this);
        });
    });

})(jQuery);
