(function($) {

    window.AsyncBlock = Class(EventedObject, function AsyncBlock(cls, superclass) {
        cls.prototype.init = function($placeholder, options) {
            superclass.prototype.init.call(this);

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

            this.$placeholder.data(cls.dataParamName, this);

            this.ajax();
        };

        /*
            Запрос блока
         */
        cls.prototype.ajax = function() {
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
        cls.prototype.ajaxSuccess = function(response) {
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
        cls.prototype.ajaxError = function(response) {
            this.$placeholder.remove();
            this.trigger('error.asyncblock', response);
        };
    });
    AsyncBlock.dataParamName = 'async-block';


    $(document).ready(function() {
        $('.async-block').each(function() {
            AsyncBlock(this);
        });
    });

})(jQuery);
