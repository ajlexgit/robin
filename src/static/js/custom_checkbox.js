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

    window.CustomCheckbox = Class(null, function(cls, superclass) {
        cls.init = function(input, options) {
            this.$input = $(input).first();
            if (!this.$input.length) {
                console.error('CustomCheckbox: input element not found');
                return false;
            }

            if (this.$input.prop('tagName') != 'INPUT') {
                console.error('CustomCheckbox: not INPUT element ');
                return false;
            }

            // отвязывание старого экземпляра
            var old_instance = this.$input.data(cls.dataParamName);
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
            this._initial_css = this.$input.get(0).style.cssText;
            this.$input.hide();

            // новый чекбокс
            this.$elem = $('<div>').insertAfter(this.$input);
            this.$elem.addClass(this.opts.className);

            // начальное состояние
            this._set_checked(this.$input.prop('checked'));
            this._set_enabled(!this.$input.prop('disabled'));


            // клик на новый элемент
            var that = this;
            this.$elem.on('click.checkbox', function() {
                that.$input.triggerHandler('change');
                return false;
            });

            this.$input.on('change.checkbox', function() {
                if (!that.is_enabled()) {
                    return false
                }

                var is_checked = that.is_checked();
                that._set_checked(!is_checked);
                that.opts.onCheck.call(that);
                that.$input.trigger('check.checkbox', [that]);

                return false;
            });

            this.$input.data(cls.dataParamName, this);
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$input.removeData(cls.dataParamName);
            this.$input.off('.checkbox');

            // восстановление CSS
            this.$input.get(0).style.cssText = this._initial_css;

            this.$elem.remove();
        };

        /*
            Установка состояния чекбокса
         */
        cls.prototype._set_checked = function(checked) {
            this._checked = Boolean(checked);
            if (this._checked) {
                this.$elem.addClass(this.opts.checkedClass);
                this.$input.prop('checked', true);
            } else {
                this.$elem.removeClass(this.opts.checkedClass);
                this.$input.prop('checked', false);
            }
        };

        /*
            Выделение
         */
        cls.prototype.check = function() {
            return this._set_checked(true)
        };

        /*
            Снятие выделения
         */
        cls.prototype.uncheck = function() {
            return this._set_checked(false)
        };

        /*
            Получение состояния
         */
        cls.prototype.is_checked = function() {
            return this._checked
        };

        /*
            Установка состояния включен / отключен
         */
        cls.prototype._set_enabled = function(enabled) {
            this._enabled = Boolean(enabled);
            if (this._enabled) {
                this.$elem.removeClass(this.opts.disabledClass);
                this.$input.prop('disabled', false);
            } else {
                this.$elem.addClass(this.opts.disabledClass);
                this.$input.prop('disabled', true);
            }
        };

        /*
            Включение
         */
        cls.prototype.enable = function() {
            return this._set_enabled(true)
        };

        /*
            Выключение
         */
        cls.prototype.disable = function() {
            return this._set_enabled(false)
        };

        /*
            Получение состояния доступности
         */
        cls.prototype.is_enabled = function() {
            return this._enabled
        };
    });
    CustomCheckbox.dataParamName = 'checkbox';


    $.fn.checkbox = function(options) {
        return this.each(function() {
            CustomCheckbox.create(this, options);
        })
    }

})(jQuery);
