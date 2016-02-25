(function($) {
    'use strict';

    // собираем все ID при инициализации в один объект,
    // чтобы запросить их одним махом.
    var mass_requests = {};


    var formatResult = function(state) {
        if (!state.id) {
            return state.text;
        }
        return state.text;
    };

    var formatSelection = function(state) {
        if (!state.id) {
            return state.text;
        }
        return state.selected_text || state.text;
    };

    var event_ns = 1;
    window.Autocomplete = Class(Object, function Autocomplete(cls, superclass) {
        cls.defaults = {
            url: '',
            depends: [],
            expressions: 'title__icontains',
            minimum_input_length: 2,
            close_on_select: true,
            multiple: false
        };

        cls.DATA_KEY = 'autocomplete';


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

            // имя элемента
            this.name = this.$elem.attr('name');
            if (!this.name) {
                return this.raise('element name attribute not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$elem.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // Поля, от которых зависит текущее поле
            var depends = this.opts.depends;
            if (typeof depends == 'string') {
                depends = depends.split(',');
            } else {
                depends = depends.concat();
            }

            if (this.name.indexOf('-') >= 0) {
                var formset_prefix = this.name.split('-').slice(0, -1).join('-');
                depends = depends.map(function(item) {
                    return document.getElementById('id_' + item.replace('__prefix__', formset_prefix));
                })
            } else {
                depends = depends.map(function(item) {
                    return document.getElementById('id_' + item);
                })
            }
            this.$depends = $(depends.filter(Boolean));

            // при изменении зависимости вызываем событие изменения на текущем элементе
            var that = this;
            this.event_ns = event_ns++;
            this.$depends.on('change.autocomplete' + this.event_ns, function() {
                that.$elem.select2('data', null);
            });

            // инициализация select2
            this.initSelect2();

            this.$elem.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.$depends.off('.autocomplete' + this.event_ns);
            this.$elem.removeData(this.DATA_KEY);
        };

        /*
            Возвращает значения, от которых зависит текущее поле
         */
        cls._parentValues = function() {
            return Array.prototype.map.call(this.$depends, function(item) {
                return $(item).val()
            }).join(';');
        };

        /*
            Инициализация Select2
         */
        cls.initSelect2 = function() {
            var that = this;
            this.$elem.select2({
                minimumInputLength: this.opts.minimum_input_length,
                closeOnSelect: this.opts.close_on_select,
                multiple: this.opts.multiple,
                dropdownCssClass: "bigdrop",
                formatResult: formatResult,
                formatSelection: formatSelection,
                allowClear: true,
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
                            values: that._parentValues(),
                            expressions: that.opts.expressions
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

                    var key = [that.opts.url].join('');
                    var record = {
                        id: id,
                        elem: that.$elem,
                        callback: callback,
                        multiple: that.opts.multiple
                    };

                    if (key in mass_requests) {
                        mass_requests[key].push(record);
                    } else {
                        mass_requests[key] = [record];
                    }
                },
                escapeMarkup: function(m) {
                    return m;
                }
            });
        };
    });


    $(document).ready(function() {
        $('.autocomplete_widget').each(function() {
            var $this = $(this);
            if (!$this.closest('.empty-form').length) {
                window.Autocomplete(this, $this.data());
            }
        });

        // Запрос собранных данных
        $.each(mass_requests, function(url, records) {
            var ids = $.unique(records.map(function(record) { return record.id }));

            $.ajax(url, {
                type: 'POST',
                dataType: "json",
                data: {
                    q: ids.join(','),
                    expressions: 'pk__in'
                },
                success: function(response) {
                    var data;
                    var result = response.result;
                    if (!result || !result.length) {
                        return
                    }

                    // формирование словаря из результатов
                    var result_dict = {};
                    $.each(result, function(i, item) {
                        result_dict[item.id] = item.text;
                    });

                    // обработка каждого поля
                    $.each(records, function(i, record) {
                        if (!record.multiple) {
                            data = {
                                id: record.id,
                                text: result_dict[record.id]
                            };
                        } else {
                            data = record.id.split(',').map($.trim).filter(Boolean).map(function(pk) {
                                return {
                                    id: pk,
                                    text: result_dict[pk]
                                }
                            });
                        }

                        record.elem.select2("data", data);
                        record.callback(data);
                    });
                },
                error: $.parseError()
            });
        });
        mass_requests = {};

        if ($.attachRelatedWidgetSupport) {
            $.attachRelatedWidgetSupport('.autocomplete_widget');
        }

        if (window.Suit) {
            Suit.after_inline.register('autocomplete_widget', function(inline_prefix, row) {
                row.find('.autocomplete_widget').each(function() {
                    window.Autocomplete(this, $(this).data());
                });
            });
        }
    });

    // фикс для джанговских кнопок добавления / редактирования ForeignKey
    $(document).on('add-related', 'input.autocomplete_widget', function(event, id, text) {
        var $input = $(this);
        var select2_object = $input.data('select2');
        if (select2_object) {
            var item = {
                id: id,
                text: text
            };

            if (select2_object.opts.multiple) {
                var data = select2_object.data();
                data.push(item);
                select2_object.data(data);
            } else {
                select2_object.data(item);
            }
        }
    }).on('change-related', 'input.autocomplete_widget', function(event, objId, text, id) {
        var $input = $(this);
        var select2_object = $input.data('select2');
        if (select2_object) {
            var item = {
                id: id,
                text: text
            };

            select2_object.data(item);
        }
    });

})(jQuery);
