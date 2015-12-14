(function($) {

    window.AsyncBlock = Class(EventedObject, function AsyncBlock(cls, superclass) {
        cls.prototype.init = function($placeholder) {
            superclass.prototype.init.call(this);

            this.$placeholder = $($placeholder).first();
            if (!this.$placeholder.length) {
                return this.raise('placeholder not found');
            }

            this.url = this.$placeholder.data('url');
            if (!this.url) {
                return this.raise('url not found');
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

            var that = this;
            return this._query = $.ajax({
                url: this.url,
                type: 'GET',
                data: {
                    referer: location.toString()
                },
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
                this.trigger('success', response, $new_block);
                this.$placeholder.remove();
            }
        };

        /*
            Ошибка получения блока
         */
        cls.prototype.ajaxError = function(response) {
            this.$placeholder.remove();
            this.trigger('error', response);
        };
    });
    AsyncBlock.dataParamName = 'async-block';


    $(document).ready(function() {
        $('.async-block').each(function() {
            AsyncBlock(this);
        });
    });

})(jQuery);
