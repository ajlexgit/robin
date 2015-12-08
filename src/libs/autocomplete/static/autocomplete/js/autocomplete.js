(function($) {

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
    window.Autocomplete = Class(null, function Autocomplete(cls, superclass) {
        cls.prototype.init = function(element, options) {
            this.$elem = $(element).first();
            if (!this.$elem.length) {
                return this.raise('element not found');
            }

            // настройки
            this.opts = $.extend({
                url: '',
                depends: [],
                expressions: 'title__icontains',
                minimum_input_length: 2,
                close_on_select: true,
                multiple: false
            }, options);

            if (!this.opts.url) {
                return this.raise('url required');
            }

            // имя элемента
            this.name = this.$elem.attr('name');
            if (!this.name) {
                return this.raise('element name attribute not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$elem.data(cls.dataParamName);
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
                that.$elem.change();
            });

            // инициализация select2
            this.initSelect2();

            this.$elem.data(cls.dataParamName, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            this.$depends.off('.autocomplete' + this.event_ns);
            this.$elem.removeData(cls.dataParamName);
        };

        /*
            Возвращает значения, от которых зависит текущее поле
         */
        cls.prototype._parentValues = function() {
            return Array.prototype.map.call(this.$depends, function(item) {
                return $(item).val()
            }).join(';');
        };

        /*
            Инициализация Select2
         */
        cls.prototype.initSelect2 = function() {
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

                    $.ajax(that.opts.url, {
                        type: 'POST',
                        dataType: "json",
                        data: {
                            q: id,
                            values: that._parentValues(),
                            expressions: that.opts.multiple ? 'pk__in' : 'pk'
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
    Autocomplete.dataParamName = 'autocomplete';


    $(document).ready(function() {
        $('.autocomplete_widget').each(function() {
            var $this = $(this);
            if (!$this.closest('.empty-form').length) {
                Autocomplete.create(this, $this.data());
            }
        });

        if ($.attachRelatedWidgetSupport) {
            $.attachRelatedWidgetSupport('.autocomplete_widget');
        }

        if (window.Suit) {
            Suit.after_inline.register('autocomplete_widget', function(inline_prefix, row) {
                row.find('.autocomplete_widget').each(function() {
                    Autocomplete.create(this, $(this).data());
                });
            });
        }
    });

    // фикс для джанговских кнопок добавления / редактирования ForeignKey
    $(document).on('change-related add-related', 'input.autocomplete_widget', function() {
        var $input = $(this);
        var select2_object = $input.data('select2');
        if (select2_object) {
            select2_object.val($input.val());
            $input.trigger('change');
        }
    });

})(jQuery);
