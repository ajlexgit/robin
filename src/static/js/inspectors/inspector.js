(function($) {

    /*
        Базовый класс инспектирования DOM-элементов.

        Требует:
            jquery.utils.js
     */

    window.Inspector = Class(null, function(cls, superclass) {
        cls.init = function() {
            this._list = [];
            this.STATE_DATA_KEY = 'inspector_state';
            this.OPTS_DATA_KEY = 'inspector_opts';
        };

        cls.prototype.getDefaultOpts = function() {
            return {
                beforeCheck: $.noop,
                afterCheck: $.noop
            }
        };

        /*
            Удаление элемента из инспектирования, если он есть
         */
        cls.prototype._ignoreElement = function($element) {
            var index = this._list.indexOf($element.get(0));
            if (index >= 0) {
                $element.removeData(this.OPTS_DATA_KEY + ' ' + this.STATE_DATA_KEY);
                this._list.splice(index, 1);
            }
        };

        /*
            Получение настроек DOM-элемента
         */
        cls.prototype.getOpts = function($element) {
            return $element.first().data(this.OPTS_DATA_KEY) || this.getDefaultOpts();
        };

        /*
            Сохранение настроек DOM-элемента
         */
        cls.prototype._setOpts = function($element, opts) {
            $element.first().data(this.OPTS_DATA_KEY, opts);
        };

        /*
            Сохранение состояния DOM-элемента
         */
        cls.prototype._setState = function($element, state) {
            $element.first().data(this.STATE_DATA_KEY, state);
        };


        // ================================================================

        cls.prototype._beforeCheck = function($element, opts) {
            opts.beforeCheck.call(this, $element, opts);
        };

        cls.prototype._check = function($element, opts) {
            throw Error('not implemented');
        };

        cls.prototype._afterCheck = function($element, opts, state) {
            opts.afterCheck.call(this, $element, opts, state);
            this._setState($element, state);
        };

        // ================================================================

        /*
            Получение состояния DOM-элемента
         */
        cls.prototype.getState = function($element) {
            return $element.first().data(this.STATE_DATA_KEY);
        };

        /*
            Функция, проверяющая некоторое условие на DOM-элементе
         */
        cls.prototype.check = function($elements, options) {
            $elements = $($elements);
            if (!$elements.length) {
                console.error('Inspector: checking elements required');
                return false;
            }

            var that = this;
            $elements.each(function(i, elem) {
                var $elem = $(elem);

                var opts = options || that.getOpts($elem);
                if (!opts) {
                    console.warn('Inspector: checking options required');
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
        cls.prototype.inspect = function($elements, options) {
            $elements = $($elements);
            if (!$elements.length) {
                console.error('Inspector: inspecting elements required');
                return false;
            }

            var opts = $.extend(this.getDefaultOpts(), options);
            if (!opts) {
                console.error('Inspector: inspecting options required');
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
        cls.prototype.ignore = function($elements) {
            $elements = $($elements);
            if (!$elements.length) {
                console.error('Inspector: ignoring elements required');
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
        cls.prototype.checkAll = function() {
            var i = 0;
            var element;
            while (element = this._list[i]) {
                this.check(element);
                i++;
            }
        };
    });

})(jQuery);