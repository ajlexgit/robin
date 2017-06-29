(function($) {

    /*
        Оптимальная разбивка элементов по колонкам.

        Зависит от:
            jquery-ui.js

        Пример:
            HTML:
                <div id="block">
                    <div class="item">...</div>
                    <div class="item">...</div>
                    ...
                    <div class="item">...</div>
                </div>

            JS:
                $('#block').columnizer({
                    columns: 2,
                    selector: '.item'
                });

                // изменение кол-ва колонок
                $('#block').columnizer('option', 'columns', 3);
     */

    $.widget("django.columnizer", {
        options: {
            columns: 2,
            selector: '',

            enable: function(event, data) {
                var that = data.widget;
                that.setColumns(that.options.columns);
                that._addClass(that.element, 'columnizer');
            },
            disable: function(event, data) {
                var that = data.widget;
                that.setColumns(0);
                that._removeClass(that.element, 'columnizer');
            },
            destroy: function(event, data) {
                var that = data.widget;
                that.setColumns(0);
                that._removeClass(that.element, 'columnizer');
            }
        },

        _create: function() {
            // запуск
            this._checkEnabled();
        },

        _setOption: function(key, value) {
            if (key === "columns" ) {
                this.setColumns(value);
            }
            this._super(key, value);
        },

        _setOptionDisabled: function(value) {
            this._super(value);
            this._checkEnabled();
        },

        _checkEnabled: function() {
            if (this.options.disabled) {
                this.trigger('disable');
            } else {
                this.trigger('enable');
            }
        },

        _destroy: function() {
            this.trigger('destroy');
        },


        /*
            Вызов событий
         */
        trigger: function(event, data) {
            this._trigger(event, null, $.extend({
                widget: this
            }, data));
        },


        /*
            Возвращает элементы для их разбивки
         */
        getItems: function() {
            return this.element.find(this.options.selector);
        },

        /*
            Возвращает массив высот элементов
         */
        getItemHeights: function($items) {
            return $items.toArray().map(function(elem) {
                return $(elem).outerHeight();
            });
        },

        /*
            Построение карты разделения элементов.
            Возвращает массив массивов, содержащих высоты элементов
         */
        getMap: function(heights, column_count) {
            // средняя высота колонки
            var average = heights.reduce(function(a, b) {
                    return a + b;
                }, 0) / column_count;

            var map = [];
            var column_index = -1;
            while (++column_index < column_count) {
                if (column_index === column_count - 1) {
                    // последняя колонка - добавляем все оставшиеся элементы
                    map.push(heights.length);
                    break;
                }

                // формируем колонку с минимальным отклонением от среднего
                var height = 0;
                var deviation = average;
                var item_index = 0;
                var total_count = heights.length;
                while (item_index < total_count) {
                    var item_height = heights[item_index];
                    var next_deviation = Math.abs(average - height - item_height);

                    // отклонение уменьшилось или это первый элемент
                    if ((next_deviation <= deviation) || !height) {
                        deviation = next_deviation;
                        height += item_height;
                        item_index++;
                    } else {
                        break
                    }
                }

                heights.splice(0, item_index);
                map.push(item_index);
            }

            return map;
        },

        /*
            Создание контейнера колонки элементов
         */
        cleateItemsColumn: function($column_items) {
            return $('<div/>').addClass('column').append($column_items);
        },

        /*
            Формирование колонок
         */
        setColumns: function(column_count) {
            // очистка контейнера
            var $items = this.getItems();
            var heights = this.getItemHeights($items);
            $items.detach();
            this.element.empty();

            column_count = parseInt(column_count);
            if (column_count <= 0) {
                // удаление колонок
                this.element.append($items);
                return [];
            }

            var map = this.getMap(heights, column_count);
            for (var i=0, l=map.length; i<l; i++) {
                this.element.append(
                    this.cleateItemsColumn($items.splice(0, map[i]))
                );
            }
            return map;
        }
    });

})(jQuery);
