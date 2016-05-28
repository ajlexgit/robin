(function($) {

    $.extend($.fn.select2.defaults, {
        closeOnSelect: true,
        dropdownCssClass: "bigdrop",
        allowClear: true,

        cache_key: function(query) {
            return {
                page: query.page,
                term: query.term
            }
        },
        calc_cache: function(query) {
            var result = [];
            var cache_key = this.cache_key(query);
            for (var key in cache_key) {
                if (cache_key.hasOwnProperty(key)) {
                    result.push(key);
                    result.push(cache_key[key].toString());
                }
            }
            return result.join(':');
        },

        query: function(query) {
            if (this.__cache == undefined) {
                this.__cache = {};
            }
            var CACHE = this.__cache;

            var cache_key = this.calc_cache(query);
            if (CACHE[cache_key]) {
                query.callback(CACHE[cache_key]);
                return
            }

            // default query function
            var options = this.ajax;
            var url = options.url;
            var transport = $.fn.select2.ajaxDefaults.transport;
            var params = $.extend({}, $.fn.select2.ajaxDefaults.params);
            var data = options.data.call(self, query.term, query.page, query.context);

            if (options.params) {
                if ($.isFunction(options.params)) {
                    $.extend(params, options.params.call(self));
                } else {
                    $.extend(params, options.params);
                }
            }

            $.extend(params, {
                url: url,
                type: options.type,
                data: data,
                dataType: options.dataType,
                success: function(data) {
                    var results = options.results(data, query.page, query);
                    CACHE[cache_key] = results;
                    query.callback(results);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    var results = {
                        hasError: true,
                        jqXHR: jqXHR,
                        textStatus: textStatus,
                        errorThrown: errorThrown
                    };

                    query.callback(results);
                }
            });
            transport.call(self, params);
        }
    })

})(jQuery);