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

    window.Radiobox = Class(null, function Radiobox(cls, superclass) {
        cls.prototype.init = function(input, options) {
            this.$root = $(input).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            if (this.$root.prop('tagName') != 'INPUT') {
                return this.raise('root element is not an input');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(cls.dataParamName);
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
            this.$elem.on('click.radiobox', function() {
                that.$root.triggerHandler('change');
                return false;
            });

            this.$root.on('change.radiobox', function() {
                if (!that.is_enabled()) {
                    return false
                }

                var is_checked = that.isChecked();
                if (is_checked) {
                    return false
                }

                that._set_checked(!is_checked);
                that.opts.onCheck.call(that);
                that.$root.trigger('check.radiobox', [that]);

                return false;
            });

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            // восстановление CSS
            this.$root.get(0).style.cssText = this._initial_css;

            this.$elem.remove();

            this.$root.off('.radiobox');
            this.$root.removeData(cls.dataParamName);
        };

        /*
            Установка состояния чекбокса
         */
        cls.prototype._set_checked = function(checked) {
            this._checked = Boolean(checked);
            if (this._checked) {
                this.$elem.addClass(this.opts.checkedClass);
                this.$root.prop('checked', true);

                var name = this.$root.attr('name');
                var $grouped = $('input[type="radio"][name="' + name + '"]').not(this.$root);
                $grouped.each(function(i, item) {
                    var $item = $(item);
                    var radiobox_obj = $item.data(cls.dataParamName);
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
                this.$root.prop('disabled', false);
            } else {
                this.$elem.addClass(this.opts.disabledClass);
                this.$root.prop('disabled', true);
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
    Radiobox.dataParamName = 'radiobox';


    $.fn.radiobox = function(options) {
        return this.each(function() {
            Radiobox(this, options);
        })
    }

})(jQuery);
