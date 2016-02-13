(function($) {

    /*
        Кастомный чекбокс, заменяющий стандартный.

        Требует:
            jquery.utils.js

        Параметры:
            className       - класс, который добавляется на новый элемент, представляющий чекбокс
            checkedClass    - класс, который добавляется на новый элемент, когда он выделен
            disabledClass   - класс, который добавляется на новый элемент, когда он отключен

        События:
            // Перед изменением состояния. Если вернет false - состояние не изменится
            before_change

            // После изменения состояния
            after_change

            // Состояние изменилоь на "выделен"
            check

            // Состояние изменилоь на "не выделен"
            uncheck

        Пример:
            $('input[type="checkbox"]').checkbox()
    */

    window.Checkbox = Class(EventedObject, function Checkbox(cls, superclass) {
        cls.defaults = {
            className: 'custom-checkbox',
            checkedClass: 'checked',
            disabledClass: 'disabled'
        };

        cls.DATA_KEY = 'checkbox';


        cls.init = function(input, options) {
            superclass.init.call(this);

            this.$input = $(input).first();
            if (!this.$input.length) {
                return this.raise('root element not found');
            }

            if (this.$input.prop('tagName') != 'INPUT') {
                return this.raise('root element is not an input');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$input.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // запоминаем CSS и скрываем стандартный чекбокс
            this._initial_css = this.$input.get(0).style.cssText;
            this.$input.hide();

            // новый чекбокс
            this.$elem = $('<div>').insertAfter(this.$input).append(this.$input);
            this.$elem.addClass(this.opts.className);

            // начальное состояние
            this._set_checked(this.$input.prop('checked'));
            this._set_enabled(!this.$input.prop('disabled'));


            // клик на новый элемент
            var that = this;
            this.$elem.on(touchClick + '.checkbox', function() {
                that.$input.triggerHandler('change');
                return false;
            });

            this.$input.on('change.checkbox', function() {
                if (that.isEnabled()) {
                    if (that.isChecked()) {
                        that.uncheck();
                    } else {
                        that.check();
                    }
                }

                return false;
            });

            this.$elem.data(this.DATA_KEY, this);
            this.$input.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            // восстановление CSS
            this.$input.get(0).style.cssText = this._initial_css;

            this.$input.off('.checkbox');
            this.$input.removeData(this.DATA_KEY);
            this.$input.insertBefore(this.$elem);
            this.$elem.remove();
            superclass.destroy.call(this);
        };

        /*
            Установка состояния чекбокса
         */
        cls._set_checked = function(checked) {
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
        cls.check = function() {
            if (!this.isChecked()) {
                if (this.trigger('before_change') === false) {
                    return this;
                }

                this._set_checked(true);
                this.trigger('check');
                this.trigger('after_change');
            }
            return this;
        };

        /*
            Снятие выделения
         */
        cls.uncheck = function() {
            if (this.isChecked()) {
                if (this.trigger('before_change') === false) {
                    return this;
                }

                this._set_checked(false);
                this.trigger('uncheck');
                this.trigger('after_change');
            }
            return this;
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
                this.$input.prop('disabled', false);
            } else {
                this.$elem.addClass(this.opts.disabledClass);
                this.$input.prop('disabled', true);
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
        cls.isEnabled = function() {
            return this._enabled
        };
    });


    $.fn.checkbox = function(options) {
        return this.each(function() {
            window.Checkbox(this, options);
        })
    }

})(jQuery);
