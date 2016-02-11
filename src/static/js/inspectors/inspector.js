(function($) {

    /*
        Базовый класс инспектирования DOM-элементов.

        Требует:
            jquery.utils.js
     */

    window.Inspector = Class(Object, function Inspector(cls, superclass) {
        cls.defaults = {
            beforeCheck: $.noop,
            afterCheck: $.noop
        };

        cls.STATE_DATA_KEY = 'inspector_state';
        cls.OPTS_DATA_KEY = 'inspector_opts';


        cls.init = function() {
            this._selectors = [];
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
            Получение состояния DOM-элемента
         */
        cls.getState = function($element) {
            return $element.first().data(this.STATE_DATA_KEY);
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
            Функция, проверяющая условие инспектирования на элементах или селекторе
         */
        cls.check = function(elements, options) {
            var that = this;

            var $elements = $(elements);
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
            Добавление селекора элементов для инспектирования
         */
        cls.inspect = function(selector, options) {
            var opts = $.extend({}, this.defaults, options);
            if (!opts) {
                return this.error('inspecting options required');
            }

            var that = this;
            var $elements = $(selector);

            // если селектор уже инспектируется - удаляем его
            this.ignore(selector);

            // инициализация состояния элементов
            $elements.each(function(i, elem) {
                var $elem = $(elem);
                that._setOpts($elem, opts);
                that._setState($elem, null);
            });

            this._selectors.push(selector.toLocaleLowerCase());

            // сразу проверяем элементы
            this.check(selector);
        };

        /*
            Удаление селектора из инспектирования
         */
        cls.ignore = function(selector) {
            var index = this._selectors.indexOf(selector);
            if (index >= 0) {
                $(selector).removeData(this.OPTS_DATA_KEY + ' ' + this.STATE_DATA_KEY);
                this._selectors.splice(index, 1);
            }
        };

        /*
            Проверка всех инспектируемых элементов
         */
        cls.checkAll = function() {
            var i = 0;
            var selector;
            while (selector = this._selectors[i++]) {
                this.check(selector);
            }
        };
    });

})(jQuery);