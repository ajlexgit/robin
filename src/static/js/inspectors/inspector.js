(function($) {

    /*
        Базовый класс инспектирования DOM-элементов.

        Требует:
            jquery.utils.js
     */

    window.Inspector = Class(null, function Inspector(cls, superclass) {
        cls.defaults = {
            beforeCheck: $.noop,
            afterCheck: $.noop
        };

        cls.STATE_DATA_KEY = 'inspector_state';
        cls.OPTS_DATA_KEY = 'inspector_opts';


        cls.init = function() {
            this._list = [];
        };

        /*
            Удаление элемента из инспектирования, если он есть
         */
        cls._ignoreElement = function($element) {
            var index = this._list.indexOf($element.get(0));
            if (index >= 0) {
                $element.removeData(this.OPTS_DATA_KEY + ' ' + this.STATE_DATA_KEY);
                this._list.splice(index, 1);
            }
        };

        /*
            Получение настроек DOM-элемента
         */
        cls.getOpts = function($element) {
            return $element.first().data(this.OPTS_DATA_KEY) || this.defaults;
        };

        /*
            Сохранение настроек DOM-элемента
         */
        cls._setOpts = function($element, opts) {
            $element.first().data(this.OPTS_DATA_KEY, opts);
        };

        /*
            Сохранение состояния DOM-элемента
         */
        cls._setState = function($element, state) {
            $element.first().data(this.STATE_DATA_KEY, state);
        };


        // ================================================================

        cls._beforeCheck = function($element, opts) {
            opts.beforeCheck.call(this, $element, opts);
        };

        cls._check = function($element, opts) {
            throw Error('not implemented');
        };

        cls._afterCheck = function($element, opts, state) {
            opts.afterCheck.call(this, $element, opts, state);
            this._setState($element, state);
        };

        // ================================================================

        /*
            Получение состояния DOM-элемента
         */
        cls.getState = function($element) {
            return $element.first().data(this.STATE_DATA_KEY);
        };

        /*
            Функция, проверяющая некоторое условие на DOM-элементе
         */
        cls.check = function($elements, options) {
            $elements = $($elements);
            if (!$elements.length) {
                this.error('checking elements required');
                return false;
            }

            var that = this;
            $elements.each(function(i, elem) {
                var $elem = $(elem);

                var opts = $.extend({}, that.getOpts($elem), options);
                if (!opts) {
                    that.error('checking options required');
                    return;
                }

                that._beforeCheck($elem, opts);
                var state = that._check($elem, opts);
                that._afterCheck($elem, opts, state);
            });
        };

        /*
            Добавление элементов для инспектирования изменения их пропорций
         */
        cls.inspect = function($elements, options) {
            $elements = $($elements);
            if (!$elements.length) {
                this.error('inspecting elements required');
                return false;
            }

            var opts = $.extend(this.getDefaultOpts(), options);
            if (!opts) {
                this.error('inspecting options required');
                return false;
            }

            var that = this;
            $elements.each(function(i, elem) {
                var $elem = $(elem);

                // если элемент уже испектируется - удаляем его
                that._ignoreElement($elem);

                // инициализация состояния
                that._setOpts($elem, opts);
                that._setState($elem, null);

                that._list.push($elem.get(0));
            });
        };

        /*
            Удаление элементов из инспектирования
         */
        cls.ignore = function($elements) {
            $elements = $($elements);
            if (!$elements.length) {
                this.error('ignoring elements required');
                return false;
            }

            var that = this;
            $elements.each(function(i, elem) {
                that._ignoreElement($(elem));
            });
        };

        /*
            Добавление элементов для инспектирования изменения их пропорций
         */
        cls.checkAll = function() {
            var i = 0;
            var element;
            while (element = this._list[i]) {
                this.check(element);
                i++;
            }
        };
    });

})(jQuery);