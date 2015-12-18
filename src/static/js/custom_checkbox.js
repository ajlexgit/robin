(function($) {

    /*
        Кастомный чекбокс, заменяющий стандартный.

        Требует:
            jquery.utils.js

        Параметры:
            className       - класс, который добавляется на новый элемент, представляющий чекбокс
            checkedClass    - класс, который добавляется на новый элемент, когда он выделен
            disabledClass   - класс, который добавляется на новый элемент, когда он отключен
            onCheck         - событие, вызываемое после включения чекбокса

        Пример:
            $('input[type="checkbox"]').checkbox()
    */

    window.Checkbox = Class(null, function Checkbox(cls, superclass) {
        cls.dataParamName = 'checkbox';

        cls.init = function(input, options) {
            this.$root = $(input).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            if (this.$root.prop('tagName') != 'INPUT') {
                return this.raise('root element is not an input');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // настройки
            this.opts = $.extend({
                className: 'custom-checkbox',
                checkedClass: 'checked',
                disabledClass: 'disabled',
                onCheck: $.noop
            }, options);

            // запоминаем CSS и скрываем чекбокс
            this._initial_css = this.$root.get(0).style.cssText;
            this.$root.hide();

            // новый чекбокс
            this.$elem = $('<div>').insertAfter(this.$root);
            this.$elem.addClass(this.opts.className);

            // начальное состояние
            this._set_checked(this.$root.prop('checked'));
            this._set_enabled(!this.$root.prop('disabled'));


            // клик на новый элемент
            var that = this;
            this.$elem.on('click.checkbox', function() {
                that.$root.triggerHandler('change');
                return false;
            });

            this.$root.on('change.checkbox', function() {
                if (!that.is_enabled()) {
                    return false
                }

                var is_checked = that.isChecked();
                that._set_checked(!is_checked);
                that.opts.onCheck.call(that);
                that.$root.trigger('check.checkbox', [that]);

                return false;
            });

            this.$root.data(this.dataParamName, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            // восстановление CSS
            this.$root.get(0).style.cssText = this._initial_css;

            this.$elem.remove();

            this.$root.off('.checkbox');
            this.$root.removeData(this.dataParamName);
        };

        /*
            Установка состояния чекбокса
         */
        cls._set_checked = function(checked) {
            this._checked = Boolean(checked);
            if (this._checked) {
                this.$elem.addClass(this.opts.checkedClass);
                this.$root.prop('checked', true);
            } else {
                this.$elem.removeClass(this.opts.checkedClass);
                this.$root.prop('checked', false);
            }
        };

        /*
            Выделение
         */
        cls.check = function() {
            return this._set_checked(true)
        };

        /*
            Снятие выделения
         */
        cls.uncheck = function() {
            return this._set_checked(false)
        };

        /*
            Получение состояния
         */
        cls.isChecked = function() {
            return this._checked
        };

        /*
            Установка состояния включен / отключен
         */
        cls._set_enabled = function(enabled) {
            this._enabled = Boolean(enabled);
            if (this._enabled) {
                this.$elem.removeClass(this.opts.disabledClass);
                this.$root.prop('disabled', false);
            } else {
                this.$elem.addClass(this.opts.disabledClass);
                this.$root.prop('disabled', true);
            }
        };

        /*
            Включение
         */
        cls.enable = function() {
            return this._set_enabled(true)
        };

        /*
            Выключение
         */
        cls.disable = function() {
            return this._set_enabled(false)
        };

        /*
            Получение состояния доступности
         */
        cls.is_enabled = function() {
            return this._enabled
        };
    });


    $.fn.checkbox = function(options) {
        return this.each(function() {
            Checkbox(this, options);
        })
    }

})(jQuery);
