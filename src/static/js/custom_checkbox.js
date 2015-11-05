(function($) {

    /*
        Кастомный чекбокс, подключаемый к стандартному.

        Пример:
            $('input[type=checkbox]').each(function() {
                CustomCheckbox.create(this);
            })

        Требует:
            jquery.utils.js
    */

    window.CustomCheckbox = Class(null, function(cls, superclass) {
        var dataParamName = 'object';
        var className = 'custom-checkbox';

        cls.init = function(input, options) {
            this.$input = $(input).first();
            if (!this.$input.length) {
                console.error('CustomCheckbox can\'t find input element');
                return false;
            }

            // настройки
            this.opts = $.extend({
                checkedClass: 'checked',
                beforeChange: $.noop
            }, options);

            // новый чекбокс
            this.$elem = $('<div>').addClass(className).insertAfter(this.$input);

            // начальное состояние
            this._set_checked(this.$input.prop('checked'));

            var that = this;
            this.$input.data(dataParamName, this).off('.checkbox').on('change.checkbox', function() {
                that._set_checked(!that.is_checked());
                return false;
            });
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$input.removeData(dataParamName).off('.checkbox');
            this.$elem.remove();
        };


        // Установка состояния
        cls.prototype._set_checked = function(value) {
            value = Boolean(value);
            if (value == this._checked) {
                return
            }

            if (this.opts.beforeChange.call(this, value) === false) {
                return
            }

            this._checked = value;

            if (this.is_checked()) {
                this.$elem.addClass(this.opts.checkedClass);
                this.$input.prop('checked', true);
            } else {
                this.$elem.removeClass(this.opts.checkedClass);
                this.$input.prop('checked', false);
            }

            return this._checked;
        };

        /*
            Получение состояния
         */
        cls.prototype.is_checked = function() {
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

})(jQuery);
