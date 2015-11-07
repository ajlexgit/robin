(function($) {

    var AutocompleteTextbox = Class(null, function(cls, superclass) {
        cls.init = function(block, options) {
            this.$block = $(block).first();
            if (!this.$block.length) {
                console.error('AutocompleteTextbox can\'t find block');
                return
            }

            this.$input = this.$block.find('input').first();
            if (!this.$input.length) {
                console.error('AutocompleteTextbox can\'t find input');
                return
            }

            this.$choices = this.$block.find('.choices').first();
            if (!this.$choices.length) {
                console.error('AutocompleteTextbox can\'t find choices');
                return
            }

            // настройки
            this.opts = $.extend({
                tags: [],
                minimumInputLength: 1,
                matcher: function(term, text) {
                    return text.toUpperCase().indexOf(term.toUpperCase()) >= 0;
                }
            }, options);

            // Массив тэгов берется из опций или из строки data-tags, с разделителем "::"
            var tags;
            if (!$.isArray(this.opts.tags)) {
                console.log('AutocompleteTextbox: tags must be an array');
                return
            } else if (this.opts.tags.length) {
                tags = this.opts.tags.concat();
            } else {
                tags = $.trim(this.$input.data('tags'));
                if (tags) {
                    tags = tags.split('::');
                } else {
                    tags = []
                }
            }
            this.tags = tags.map($.trim);

            // Текст активного элемента списка
            this.active_text = null;

            this.$block.data(AutocompleteTextbox.dataParamName, this);
        };

        /*
            Фильтрация массива по строке
         */
        cls.prototype.grep = function(array, term) {
            var that = this;
            return $.grep(array, function(item) {
                return that.opts.matcher(term,  item)
            })
        };

        /*
            Получение отфильтрованных тэгов
         */
        cls.prototype.get_matched_tags = function() {
            var term = $.trim(this.$input.val());
            return this.grep(this.tags, term);
        };

        /*
            Построение списка
         */
        cls.prototype.render_tags = function(tags) {
            var result = '<ul>';
            for (var i = 0, l = tags.length; i < l; i++) {
                result += '<li>' + tags[i] + '</li>';
            }
            result += '</ul>';
            this.$choices.html(result);
        };

        /*
            Открыт ли список
         */
        cls.prototype.is_opened = function() {
            return this.$block.hasClass('opened');
        };

        /*
            Установка активного элемента списка
         */
        cls.prototype.set_active_text = function($item) {
            if (!$item || !$item.length) {
                this.active_text = null;
                return
            }

            $item.siblings('li.active').removeClass('active');
            $item.addClass('active');
            this.active_text = $.trim($item.text());

            // прокрутка
            var $list = this.$choices.find('ul').first();
            var list_top = $list.scrollTop();
            var list_bottom = list_top + $list.height();
            var item_top = list_top + $item.position().top;
            var item_bottom = item_top + $item.outerHeight();
            if ((item_top >= list_top) && (item_bottom <= list_bottom)) {
                // элемент виден
            } else {
                if (item_top < list_top) {
                    $list.scrollTop(item_top);
                } else {
                    $list.scrollTop(item_bottom - $list.height());
                }
            }
        };

        /*
            Поиск активного элемента списка
         */
        cls.prototype.get_active_item = function() {
            var regexp = new RegExp('^' + this.active_text + '$');
            var $items = this.$choices.find('li').filter(function() {
                return regexp.test($.trim($(this).text()))
            });

            return $items.first();
        };

        /*
            Показ списка
         */
        cls.prototype.show_list = function() {
            var tags = this.get_matched_tags();
            if (!tags || !tags.length) {
                this.close_list();
                return
            }
            this.render_tags(tags);

            var input_width = this.$input.get(0).style.width;
            this.$choices.css({
                width: input_width,
                paddingTop: this.$input.outerHeight() + 4
            });

            // Открытие и активация пункта списка
            if (this.is_opened()) {
                var $active = this.get_active_item();
                if ($active.length) {
                    this.set_active_text($active);
                } else {
                    this.set_active_text(this.$choices.find('li:first'));
                }
            } else {
                this.set_active_text(this.$choices.find('li:first'));
                this.$block.addClass('opened');
            }

            // Закрытие списка после клика
            var that = this;
            $(document).off('click.autocomplete_textbox').on('click.autocomplete_textbox', function(event) {
                var target = $(event.target);
                if (!target.closest(that.$choices).length && !target.closest(that.$input).length) {
                    that.close_list();
                }
            });
        };

        /*
            Закрытие списка
         */
        cls.prototype.close_list = function() {
            $(document).off('click.autocomplete_textbox');
            this.$block.removeClass('opened');
            this.set_active_text(null);
        };
    });
    AutocompleteTextbox.dataParamName = 'autocomplete_textbox';


    /*
        Вызов события text-changed при изменении текста
     */
    $(document).on('keydown', '.autocomplete_textbox input', function(event) {
        if (event.which == 13) {
            return
        }

        var $input = $(this);
        var old_val = $.trim($input.val());
        setTimeout(function() {
            var new_val = $.trim($input.val());
            if (old_val != new_val) {
                $input.trigger('text-changed.autocomplete_textbox');
            }
        }, 0);
    });


    // Показ списка
    $(document).on('focus text-changed.autocomplete_textbox', '.autocomplete_textbox input', function() {
        var obj = $(this).closest('.autocomplete_textbox').data(AutocompleteTextbox.dataParamName);
        obj.show_list();
    });


    // Наведение на пункт списка
    $(document).on('mouseenter', '.autocomplete_textbox .choices li', function() {
        var $item = $(this);
        var obj = $item.closest('.autocomplete_textbox').data(AutocompleteTextbox.dataParamName);
        obj.set_active_text($item);
    });


    // Клик на пункт списка
    $(document).on('click', '.autocomplete_textbox .choices li', function() {
        var $item = $(this);
        var obj = $item.closest('.autocomplete_textbox').data(AutocompleteTextbox.dataParamName);
        obj.set_active_text($item);
        obj.$input.val(obj.active_text);
        obj.close_list();
    });


    // Нажатие клавиш на поле ввода
    $(document).on('keydown', '.autocomplete_textbox input', function(event) {
        var obj = $(this).closest('.autocomplete_textbox').data(AutocompleteTextbox.dataParamName);
        if (!obj.is_opened()) {
            return;
        }

        var $active_item;
        if (event.which == 40) {
            // вниз
            $active_item = obj.get_active_item();
            var $next_item = $active_item.next('li');
            if ($next_item.length) {
                obj.set_active_text($next_item);
            }
            return false;
        } else if (event.which == 38) {
            // вверх
            $active_item = obj.get_active_item();
            var $prev_item = $active_item.prev('li');
            if ($prev_item.length) {
                obj.set_active_text($prev_item);
            }
            return false;
        } else if (event.which == 13) {
            // enter
            obj.$input.val(obj.active_text);
            obj.close_list();
            return false;
        }
    });

    $(document).ready(function() {
        $('.autocomplete_textbox').each(function() {
            if (!$(this).closest('.empty-form').length) {
                AutocompleteTextbox.create(this);
            }
        });

        // Скролл списка
        $(document).on('mousewheel', '.autocomplete_textbox .choices', function(event) {
            var $ul = $(this).find('ul').first();
            var initial_top = $ul.scrollTop();
            if (event.deltaY < 0) {
                // вниз
                $ul.stop(true, true).animate({
                    scrollTop: initial_top + 44
                }, 50);
            } else {
                // вверх
                $ul.stop(true, true).animate({
                    scrollTop: initial_top - 44
                }, 50);
            }
            return false;
        });

        if (window.Suit) {
            Suit.after_inline.register('autocomplete_textbox', function(inline_prefix, row) {
                row.find('.autocomplete_textbox').each(function() {
                    AutocompleteTextbox.create(this);
                });
            });
        }
    });

})(jQuery);
