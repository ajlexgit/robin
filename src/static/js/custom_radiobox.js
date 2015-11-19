(function($) {

    /*
        Кастомный радиобокс, подключаемый к стандартному.

        Требует:
            jquery.utils.js

        Параметры:
            className       - класс, который добавляется на новый элемент, представляющий радиобокс
            checkedClass    - класс, который добавляется на новый элемент, когда он выделен
            disabledClass   - класс, который добавляется на новый элемент, когда он отключен
            beforeChange    - событие перед изменением состояния радиобокса
            afterChange     - событие после изменения состояния радиобокса

        Пример:
            $('input[type="radio"]').radiobox()
    */

    window.CustomRadiobox = Class(null, function(cls, superclass) {
        cls.init = function(input, options) {
            this.$input = $(input).first();
            if (!this.$input.length) {
                console.error('CustomRadiobox can\'t find input element');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$input.data(cls.dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$input.data(cls.dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                className: 'custom-radiobox',
                checkedClass: 'checked',
                disabledClass: 'disabled',
                beforeChange: $.noop,
                afterChange: $.noop
            }, options);

            // скрываем радиобокс
            this.$input.hide();

            // новый радиобокс
            this.$elem = $('<div>').insertAfter(this.$input);
            this.$elem.addClass(this.opts.className);

            // начальное состояние
            this._set_checked(this.$input.prop('checked'));
            this._set_disabled(this.$input.prop('disabled'));

            var that = this;

            // клик на новый элемент
            this.$elem.on('click.radiobox', function() {
                that.$input.change();
                return false;
            });

            // изменение состояния
            this.$input.on('change.radiobox', function() {
                that._set_checked(!that.checked());
                return false;
            });
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$input.removeData(cls.dataParamName);
            this.$input.off('.radiobox');
            this.$elem.remove();
        };

        /*
            Установка состояния
          */
        cls.prototype._set_checked = function(value) {
            if (this.disabled()) {
                return
            }

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

                var name = this.$input.attr('name');
                var $groupBoxes = $('input[name="' + name + '"]').not(this.$input);
                $groupBoxes.each(function(i, item) {
                    var box = $(item).data(cls.dataParamName);
                    if (box) {
                        box.uncheck()
                    }
                });

                // jQuery event
                this.$input.trigger('checked.radiobox', [this]);
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

        /*
            Установка состояния включен / отключен
         */
        cls.prototype._set_disabled = function(value) {
            value = Boolean(value);
            if (value == this._disabled) {
                return
            }

            this._disabled = value;

            if (this.disabled()) {
                this.$elem.addClass(this.opts.disabledClass);
                this.$input.prop('disabled', true);
            } else {
                this.$elem.removeClass(this.opts.disabledClass);
                this.$input.prop('disabled', false);
            }

            return this._disabled;
        };

        /*
            Получение состояния включен / отключен
         */
        cls.prototype.disabled = function() {
            return this._disabled
        };

        /*
            Включение
         */
        cls.prototype.enable = function() {
            return this._set_disabled(false)
        };

        /*
            Выключение
         */
        cls.prototype.disable = function() {
            return this._set_disabled(true)
        };
    });
    CustomRadiobox.dataParamName = 'radiobox';


    $.fn.radiobox = function(options) {
        return this.each(function() {
            CustomRadiobox.create(this, options);
        })
    }

})(jQuery);
