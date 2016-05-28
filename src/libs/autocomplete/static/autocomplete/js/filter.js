(function($) {
    'use strict';

    window.AutocompleteFilter = Class(Object, function AutocompleteFilter(cls, superclass) {
        cls.defaults = {
            url: '',
            multiple: false,
            expression: 'title__icontains',
            minimum_input_length: 2
        };

        cls.DATA_KEY = 'autocomplete_filter';

        cls.init = function(element, options) {
            this.$elem = $(element).first();
            if (!this.$elem.length) {
                return this.raise('element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            if (!this.opts.url) {
                return this.raise('url required');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$elem.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // инициализация select2
            this.initSelect2();

            this.$elem.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.$elem.removeData(this.DATA_KEY);
            this.$elem.select2('destroy');
        };

        /*
            Инициализация Select2
         */
        cls.initSelect2 = function() {
            var that = this;
            this.$elem.select2({
                multiple: this.opts.multiple,
                minimumInputLength: this.opts.minimum_input_length,
                ajax: {
                    url: this.opts.url,
                    type: 'POST',
                    quietMillis: 1,
                    dataType: 'json',
                    data: function(term, page, page_limit) {
                        return {
                            q: term,
                            page_limit: page_limit || 30,
                            page: page,
                            expression: that.opts.expression
                        };
                    },
                    results: function(data, page) {
                        return {
                            results: data.result,
                            more: (page * 30) < data.total
                        };
                    }
                },
                initSelection: function(element, callback) {
                    var id = that.$elem.val();
                    if (!id) {
                        return
                    }

                    $.ajax(that.opts.url, {
                        type: 'POST',
                        dataType: "json",
                        data: {
                            q: id,
                            expression: 'pk__in'
                        },
                        success: function(response) {
                            if (that.opts.multiple) {
                                response = response.result;
                            } else {
                                response = response.result.shift();
                            }
                            that.$elem.select2("data", response);
                            callback(response);
                        }
                    });
                },
                escapeMarkup: function(m) {
                    return m;
                }
            });
        };
    });


    $(document).ready(function() {
        $('.autocomplete-filter').each(function() {
            var $input = $(this);
            var input_data = $input.data();

            window.AutocompleteFilter($input, {
                url: input_data.url,
                multiple: Boolean(parseInt(input_data.multiple)),
                expression: input_data.expression,
                minimum_input_length: input_data.minimum_input_length
            });
        })
    });

})(jQuery);