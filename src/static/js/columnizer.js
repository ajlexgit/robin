(function($) {

    /*
        Разбивка элементов по колонкам, оборачивая элементы каждой колонки в <div>.

        Пример:
            HTML:
                <div id="block">
                    <div class="item">...</div>
                    <div class="item">...</div>
                    ...
                    <div class="item">...</div>
                </div>

            JS:
                var columnizer = Columnizer('#block', '.item');
                columnizer.setColumns(5);
     */
    window.Columnizer = Class(Object, function Columnizer(cls, superclass) {
        cls.defaults = {
            selector: '.item'
        };

        cls.COLUMN_CLASS = 'column';
        cls.DATA_KEY = 'columns';

        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            if (typeof options === 'string') {
                options = {
                    selector: options
                }
            }

            this.opts = $.extend({}, this.defaults, options);
            if (!this.opts.selector) {
                return this.raise('selector required');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            this.$root.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.setColumns(0);
            this.$root.removeData(this.DATA_KEY);
        };

        /*
            Получение элементов
         */
        cls.getItems = function() {
            return this.$root.find(this.opts.selector);
        };

        /*
            Получение высот элементов
         */
        cls.getItemHeights = function($items) {
            return $items.toArray().map(function(elem) {
                return $(elem).outerHeight();
            });
        };

        /*
            Получение карты разбиения
         */
        cls.getMap = function(heights, column_count) {
            // средняя высота колонки
            var mediana = heights.reduce(function(a, b) {
                    return a + b;
                }, 0) / column_count;

            // первоначальное разбиение
            var columns = [];
            var column_index = 0;
            while (column_index < column_count) {
                if (column_index === column_count - 1) {
                    // последняя колонка
                    columns.push(heights);
                    break;
                }

                // колонка с минимальным отклонением от медианы
                var item_index = 0;
                var column_sum = 0;
                var column_diff = mediana;
                var item_count = heights.length;
                while (item_index < item_count) {
                    var item_height = heights[item_index];
                    var next_diff = Math.abs(mediana - column_sum - item_height);

                    // не менее одного элемента в колонке
                    if (!column_sum || (next_diff <= column_diff)) {
                        column_diff = next_diff;
                        column_sum += item_height;
                        item_index++;
                    } else {
                        break
                    }
                }
                columns.push(heights.splice(0, item_index));

                column_index++;
            }

            return columns;
        };

        /*
            Разбивка на колонки
         */
        cls.setColumns = function(column_count) {
            var $items = this.getItems();
            var heights = this.getItemHeights($items);

            $items.detach();
            this.$root.empty();

            column_count = parseInt(column_count);
            if (column_count <= 0) {
                // удаление колонок
                this.$root.append($items);
                return [];
            } else {
                var map = this.getMap(heights, column_count);
                for (var i = 0, l = map.length; i < l; i++) {
                    var $column = $('<div>').addClass(this.COLUMN_CLASS);
                    $column.append($items.splice(0, map[i].length));
                    this.$root.append($column);
                }
                return map;
            }
        }
    });

})(jQuery);
