(function($) {

    var bind_autocomplete_widget = function(elements) {
        elements.each(function() {
            var self = $(this),
                name = self.attr('name'),
                self_data = self.data();

            // Форматирование имен
            var parent_ids = self_data.depends.split(',');
            if (name.indexOf('-') >= 0) {
                var formset_prefix = name.split('-').slice(0, -1).join('-');
                parent_ids = parent_ids.map(function(item) {
                    return item.replace('__prefix__', formset_prefix);
                })
            }

            var parents = parent_ids.map(function(parent_id) {
                return $('#id_' + parent_id).on('change', function() {
                    self.change();
                });
            });

            var that = this;
            self.select2({
                minimumInputLength: self_data.minimum_input_length,
                closeOnSelect: parseInt(self_data.close_on_select) || 0,
                multiple: self_data.multiple,
                allowClear: true,
                width: 280,
                ajax: {
                    url: self_data.url,
                    type: 'POST',
                    quietMillis: 1,
                    dataType: 'json',
                    data: function(term, page, page_limit) {
                        var data = {
                            q: term,
                            page_limit: page_limit || 30,
                            page: page,
                            expressions: self_data.expressions
                        };

                        if (parents.length) {
                            data.values = parents.map(function(item) {
                                return item.val()
                            }).join(';');
                        }
                        return data;
                    },
                    transport: function(params) {
                        var page = parseInt(params.data.page);
                        if (that._cache && that._cache[page]) {
                            params.success(that._cache[page]);
                        } else {
                            return $.ajax(params);
                        }
                    },
                    results: function(data, page) {
                        // Сохранение в кэш
                        if (!that._cache) {
                            that._cache = {}
                        }

                        that._cache[page] = data;
                        return {
                            results: data.result,
                            more: (page * 30) < data.total
                        };
                    }
                },
                initSelection: function(element, callback) {
                    var id = $(element).val();
                    if (id !== "") {
                        var data = {
                            q: id,
                            expressions: self_data.multiple ? 'pk__in' : 'pk'
                        };

                        if (parents.length) {
                            data.values = parents.map(function(item) {
                                return item.val()
                            }).join(';');
                        }

                        $.ajax(self_data.url, {
                            type: 'POST',
                            dataType: "json",
                            data: data,
                            success: function(response) {
                                if (self_data.multiple) {
                                    response = response.result;
                                } else {
                                    response = response.result.shift();
                                }
                                $(element).select2("data", response);
                                callback(response);
                            }
                        })
                    }
                },
                dropdownCssClass: "bigdrop",
                escapeMarkup: function(m) {
                    return m;
                }
            });
        })
    };

    $(document).ready(function() {
        $('.autocomplete_widget').each(function() {
            var self = $(this);
            if (!self.closest('.empty-form').length) {
                bind_autocomplete_widget(self);
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('autocomplete_widget', function(inline_prefix, row) {
                bind_autocomplete_widget(row.find('.autocomplete_widget'));
            });
        }

        // add popup callback
        var oldDismissAddAnotherPopup = window.dismissAddAnotherPopup;
        window.dismissAddAnotherPopup = function(win, newId, newRepr) {
            newId = html_unescape(newId);
            var name = windowname_to_id(win.name);
            var $elem = $('#' + name);
            if ($elem.length && $elem.hasClass('autocomplete_widget')) {
                var select2 = $elem.data('select2');
                if (select2.opts.multiple) {
                    var initial = select2.val() || [];
                    initial.push(newId);
                    select2.val(initial);
                } else {
                    select2.val(newId);
                }

                win.close();
                return;
            }

            oldDismissAddAnotherPopup(win, newId, newRepr);
        }
    });

})(jQuery);
