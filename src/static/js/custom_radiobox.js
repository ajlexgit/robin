(function($) {

    /*
        Кастомный радиобокс, заменяющий стандартный.

        Требует:
            jquery.utils.js

        Параметры:
            className       - класс, который добавляется на новый элемент, представляющий радиобокс
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
            $('input[type="radio"]').radiobox()
    */

    window.Radiobox = Class(EventedObject, function Radiobox(cls, superclass) {
        cls.defaults = {
            className: 'custom-radiobox',
            checkedClass: 'checked',
            disabledClass: 'disabled'
        };

        cls.DATA_KEY = 'radiobox';


        cls.init = function(input, options) {
            superclass.init.call(this);
            this.$root = $(input).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            if (this.$root.prop('tagName') != 'INPUT') {
                return this.raise('root element is not an input');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // запоминаем CSS и скрываем стандартный радиобокс
            this._initial_css = this.$root.get(0).style.cssText;
            this.$root.hide();

            // новый радиобокс
            this.$elem = $('<div>').insertAfter(this.$root);
            this.$elem.addClass(this.opts.className);

            // начальное состояние
            this._set_checked(this.$root.prop('checked'));
            this._set_enabled(!this.$root.prop('disabled'));


            // клик на новый элемент
            var that = this;
            this.$elem.on(touchClick + '.radiobox', function() {
                that.$root.triggerHandler('change');
                return false;
            });

            this.$root.on('change.radiobox', function() {
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
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            // восстановление CSS
            this.$root.get(0).style.cssText = this._initial_css;

            this.$elem.remove();
            this.$root.off('.radiobox');
            superclass.destroy.call(this);
        };

        /*
            Установка состояния чекбокса
         */
        cls._set_checked = function(checked) {
            this._checked = Boolean(checked);
            if (this._checked) {
                this.$elem.addClass(this.opts.checkedClass);
                this.$root.prop('checked', true);

                var that = this;
                var name = this.$root.attr('name');
                var $grouped = $('input[type="radio"][name="' + name + '"]').not(this.$root);
                $grouped.each(function(i, item) {
                    var $item = $(item);
                    var radiobox_obj = $item.data(that.DATA_KEY);
                    if (radiobox_obj) {
                        radiobox_obj.uncheck()
                    }
                });
            } else {
                this.$elem.removeClass(this.opts.checkedClass);
                this.$root.prop('checked', false);
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
        cls.isEnabled = function() {
            return this._enabled
        };
    });


    $.fn.radiobox = function(options) {
        return this.each(function() {
            window.Radiobox(this, options);
        })
    }

})(jQuery);
