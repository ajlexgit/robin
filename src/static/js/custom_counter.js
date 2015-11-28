(function($) {

    /*
        Кастомное поле ввода чисел, которое подключется к обёртке над
        стандартным полем input[type="number"]

        Требует:
            jquery.utils.js

        Параметры:
            buttonClass      - класс, добавляемый кнопкам
            inputClass       - класс, добавляемый полю
            min              - минимальное значение поля (перезапишет аттрибут)
            max              - максимальное значение поля (перезапишет аттрибут)
            beforeChange     - событие перед изменением значения
            afterChange      - событие после изменения значения

        Пример:
            <div class="custom-counter">
                <input type="number" value="1">
            </div>

            $('.custom-counter').counter()
    */

    window.CustomCounter = Class(null, function(cls, superclass) {
        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('CustomCounter: root element not found');
                return false;
            }

            // настройки
            this.opts = $.extend({
                buttonClass: 'custom-counter-button',
                inputClass: 'custom-counter-input',
                min: '',
                max: '',
                beforeChange: $.noop,
                afterChange: $.noop
            }, options);

            // поле
            this.$input = this.$root.find('input').first();
            if (!this.$input.length) {
                console.error('CustomCounter: input element not found');
                return false;
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // создаем кнопки
            this.$decrBtn = $('<div>').text('-').insertBefore(this.$input);
            this.$incrBtn = $('<div>').text('+').insertAfter(this.$input);

            // вешаем классы
            this.$input.addClass(this.opts.inputClass);
            this.$decrBtn.addClass(this.opts.buttonClass + ' decr');
            this.$incrBtn.addClass(this.opts.buttonClass + ' incr');

            // границы значений
            this.min = Number($.isNumeric(this.opts.min) ? this.opts.min : this.$input.prop('min'));
            this.max = Number($.isNumeric(this.opts.max) ? this.opts.max : this.$input.prop('max'));
            if (this.$input.prop('type') == 'number') {
                this.$input.prop('min', this.min);
                this.$input.prop('max', this.max);
                this.$input.prop('step', 1);
            }

            // форматируем текущее значение
            this._set_value(this.$input.val());


            // уменьшение значения
            var that = this;
            this.$decrBtn.on('click.counter', function() {
                var current = that._value || 0;
                that.value(current - 1);
                return false;
            });

            // увеличение значения
            this.$incrBtn.on('click.counter', function() {
                var current = that._value || 0;
                that.value(current + 1);
                return false;
            });

            // форматирование значения при потере фокуса
            this.$input.on('blur.counter', function() {
                that.value(that.$input.val());
            }).on('keypress.counter', function(e) {
                if (e.which == 13) {
                    that.value(that.$input.val());
                }
            });

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$decrBtn.remove();
            this.$incrBtn.remove();
            this.$input.off('.counter');
            this.$root.removeData(cls.dataParamName);
        };

        /*
            Форматирование значения
         */
        cls.prototype._formatted = function(value) {
            value = parseInt(value);
            if (isNaN(value)) {
                return value;
            }

            if ($.isNumeric(this.min)) {
                value = Math.max(value, this.min);
            }

            if ($.isNumeric(this.max)) {
                value = Math.min(value, this.max);
            }

            return value
        };

        /*
            Запись значения в input
         */
        cls.prototype._set_value = function(value) {
            this._value = this._formatted(value);
            this.$input.val(isNaN(this._value) ? '' : this._value);
        };

        /*
            Получение и установка значения
         */
        cls.prototype.value = function(value) {
            if (value === undefined) {
                return this._formatted(this.$input.val());
            }

            value = this._formatted(value);
            if (isNaN(value) && isNaN(this._value)) {
                this._set_value(value);
            } else if (value !== this._value) {
                if (this.opts.beforeChange.call(this, value) === false) {
                    return
                }

                this._set_value(value);

                this.opts.afterChange.call(this, value);
            } else {
                this._set_value(value);
            }
        };
    });
    CustomCounter.dataParamName = 'counter';


    $.fn.counter = function(options) {
        return this.each(function() {
            CustomCounter.create(this, options);
        })
    }

})(jQuery);
