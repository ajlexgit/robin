(function($) {

    /*
        Кастомный радиобокс, заменяющий стандартный.

        Требует:
            jquery.utils.js

        Параметры:
            className       - класс, который добавляется на новый элемент, представляющий радиобокс
            checkedClass    - класс, который добавляется на новый элемент, когда он выделен
            disabledClass   - класс, который добавляется на новый элемент, когда он отключен
            onCheck         - событие, вызываемое после включения радиобокса

        Пример:
            $('input[type="radio"]').radiobox()
    */

    window.CustomRadiobox = Class(null, function(cls, superclass) {
        cls.init = function(input, options) {
            this.$input = $(input).first();
            if (!this.$input.length) {
                console.error('CustomRadiobox: input element not found');
                return false;
            }

            if (this.$input.prop('tagName') != 'INPUT') {
                console.error('CustomRadiobox: not INPUT element ');
                return false;
            }

            // отвязывание старого экземпляра
            var old_instance = this.$input.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // настройки
            this.opts = $.extend({
                className: 'custom-radiobox',
                checkedClass: 'checked',
                disabledClass: 'disabled',
                onCheck: $.noop
            }, options);

            // запоминаем CSS и скрываем радиобокс
            this._initial_css = this.$input.get(0).style.cssText;
            this.$input.hide();

            // новый радиобокс
            this.$elem = $('<div>').insertAfter(this.$input);
            this.$elem.addClass(this.opts.className);

            // начальное состояние
            this._set_checked(this.$input.prop('checked'));
            this._set_enabled(!this.$input.prop('disabled'));


            // клик на новый элемент
            var that = this;
            this.$elem.on('click.radiobox', function() {
                that.$input.triggerHandler('change');
                return false;
            });

            this.$input.on('change.radiobox', function() {
                if (!that.is_enabled()) {
                    return false
                }

                var is_checked = that.isChecked();
                if (is_checked) {
                    return false
                }

                that._set_checked(!is_checked);
                that.opts.onCheck.call(that);
                that.$input.trigger('check.radiobox', [that]);

                return false;
            });

            this.$input.data(cls.dataParamName, this);
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            // восстановление CSS
            this.$input.get(0).style.cssText = this._initial_css;

            this.$elem.remove();

            this.$input.off('.radiobox');
            this.$input.removeData(cls.dataParamName);
        };

        /*
            Установка состояния чекбокса
         */
        cls.prototype._set_checked = function(checked) {
            this._checked = Boolean(checked);
            if (this._checked) {
                this.$elem.addClass(this.opts.checkedClass);
                this.$input.prop('checked', true);

                var name = this.$input.attr('name');
                var $grouped = $('input[type="radio"][name="' + name + '"]').not(this.$input);
                $grouped.each(function(i, item) {
                    var $item = $(item);
                    var radiobox_obj = $item.data(cls.dataParamName);
                    if (radiobox_obj) {
                        radiobox_obj.uncheck()
                    }
                });
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
        cls.prototype.isChecked = function() {
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
    CustomRadiobox.dataParamName = 'radiobox';


    $.fn.radiobox = function(options) {
        return this.each(function() {
            CustomRadiobox.create(this, options);
        })
    }

})(jQuery);
