(function($) {

    /*
        Кастомный чекбокс, подключаемый к стандартному.

        Требует:
            jquery.utils.js

        Параметры:
            className       - класс, который добавляется на новый элемент, представляющий чекбокс
            checkedClass    - класс, который добавляется на новый элемент, когда он выделен
            beforeChange    - событие перед изменением состояния чекбокса
            afterChange     - событие после изменения состояния чекбокса

        Пример:
            $('input[type=checkbox]').checkbox()
    */

    window.CustomCheckbox = Class(null, function(cls, superclass) {
        var dataParamName = 'object';

        cls.init = function(input, options) {
            this.$input = $(input).first();
            if (!this.$input.length) {
                console.error('CustomCheckbox can\'t find input element');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$input.data(dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$input.data(dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                className: 'custom-checkbox',
                checkedClass: 'checked',
                beforeChange: $.noop,
                afterChange: $.noop
            }, options);

            // скрываем чекбокс
            this.$input.hide();

            // новый чекбокс
            this.$elem = $('<div>').insertAfter(this.$input);
            this.$elem.addClass(this.opts.className);

            // начальное состояние
            this._set_checked(this.$input.prop('checked'));

            var that = this;

            // клик на новый элемент
            this.$elem.on('click.checkbox', function() {
                that.$input.change();
                return false;
            });

            // изменение состояния
            this.$input.on('change.checkbox', function() {
                that._set_checked(!that.checked());
                return false;
            });
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$input.removeData(dataParamName);
            this.$input.off('.checkbox');
            this.$elem.remove();
        };


        // Установка состояния
        cls.prototype._set_checked = function(value) {
            value = Boolean(value);
            if (value == this._checked) {
                return
            }

            // callback
            if (this.opts.beforeChange.call(this, value) === false) {
                return
            }

            this._checked = value;

            if (this.checked()) {
                this.$elem.addClass(this.opts.checkedClass);
                this.$input.prop('checked', true);
            } else {
                this.$elem.removeClass(this.opts.checkedClass);
                this.$input.prop('checked', false);
            }

            // callback
            this.opts.afterChange.call(this, value);

            return this._checked;
        };

        /*
            Получение состояния
         */
        cls.prototype.checked = function() {
            return this._checked
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
    });


    $.fn.checkbox = function(options) {
        return this.each(function() {
            CustomCheckbox.create(this, options);
        })
    }

})(jQuery);
