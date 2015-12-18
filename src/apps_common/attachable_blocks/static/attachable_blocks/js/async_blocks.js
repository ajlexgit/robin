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
        cls.dataParamName = 'async-block';

        cls.init = function($placeholder, options) {
            superclass.init.call(this);

            this.$placeholder = $($placeholder).first();
            if (!this.$placeholder.length) {
                return this.raise('placeholder not found');
            }

            this.opts = $.extend({
                url: window.js_storage.async_block,
                extraData: function() {
                    return {
                        block_id: this.$placeholder.data('id')
                    }
                }
            }, options);

            if (!this.opts.url) {
                return this.raise('url is empty');
            }

            this.$placeholder.data(this.dataParamName, this);

            this.ajax();
        };

        /*
            Запрос блока
         */
        cls.ajax = function() {
            if (this._query) {
                this._query.abort();
            }

            var data = $.extend({
                referer: location.toString()
            }, this.opts.extraData.call(this));

            var that = this;
            return this._query = $.ajax({
                url: this.opts.url,
                type: 'GET',
                data: data,
                dataType: 'json',
                success: function(response) {
                    that.ajaxSuccess.call(that, response);
                },
                error: function(xhr) {
                    var response = {};
                    if (xhr.responseText) {
                        response = $.parseJSON(response.responseText);
                    }
                    that.ajaxError.call(that, response);
                }
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
            this.$placeholder.remove();
            this.trigger('error.asyncblock', response);
        };
    });


    $(document).ready(function() {
        $('.async-block').each(function() {
            AsyncBlock(this);
        });
    });

})(jQuery);
