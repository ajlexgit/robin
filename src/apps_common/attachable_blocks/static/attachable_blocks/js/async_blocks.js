(function($) {

    /*
        Загрузчик асинхронных блоков.

        Требует:
            jquery.utils.js

        Ищет все элементы с классом "async-block",
        отправляет для каждого блока AJAX-запрос на получение
        HTML-кода блока. Результат заменяет исходный элемент.
     */

    window.AsyncBlock = Class(EventedObject, function AsyncBlock(cls, superclass) {
        cls.defaults = {
            url: window.js_storage.ajax_attached_block,
            extraData: function() {
                return {
                    block_id: this.$placeholder.data('id')
                }
            }
        };

        cls.DATA_KEY = 'async-block';


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
                referer: location.href
            }, this.opts.extraData.call(this));

            var that = this;
            return this._query = $.ajax({
                url: this.opts.url,
                type: 'GET',
                data: data,
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
                this.trigger('success.asyncblock', response, $new_block);
                this.$placeholder.remove();
            }
        };

        /*
            Ошибка получения блока
         */
        cls.ajaxError = function(response) {
            this.trigger('error.asyncblock', response);
            this.$placeholder.remove();
        };
    });


    $(document).ready(function() {
        $('.async-block').each(function() {
            window.AsyncBlock(this);
        });
    });

})(jQuery);
