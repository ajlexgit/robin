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
                wrapperClass: 'custom-counter-wrapper',
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
            var old_instance = this.$input.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // создаем кнопки и обертку
            this.$wrapper = $('<div>').addClass(this.opts.wrapperClass);
            this.$wrapper.prependTo(this.$root).append(this.$input);
            this.$decrBtn = $('<div>').insertBefore(this.$input);
            this.$incrBtn = $('<div>').insertAfter(this.$input);

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
                that.decrement();
                return false;
            });

            // увеличение значения
            this.$incrBtn.on('click.counter', function() {
                that.increment();
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

            this.$input.data(cls.dataParamName, this);
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$decrBtn.remove();
            this.$incrBtn.remove();
            this.$input.removeClass(this.opts.inputClass);
            this.$input.prependTo(this.$root);
            this.$input.off('.counter');
            this.$wrapper.remove();
            this.$input.removeData(cls.dataParamName);
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

        /*
            Инкремент значения
         */
        cls.prototype.increment = function() {
            var current = this._value || 0;
            this.value(current + 1);
        };

        /*
            Декремент значения
         */
        cls.prototype.decrement = function() {
            var current = this._value || 0;
            this.value(current - 1);
        };
    });
    CustomCounter.dataParamName = 'counter';


    /*
        Скролл поля изменяет значение
     */
    $(document).on('mousewheel.counter', '.custom-counter-wrapper', function(e) {
        var obj = $(this).find('input').data(CustomCounter.dataParamName);
        if (!obj) {
            return
        }

        if (e.deltaY < 0) {
            // вниз
            obj.decrement();
        } else {
            // вверх
            obj.increment();
        }

        return false
    });


    $.fn.counter = function(options) {
        return this.each(function() {
            CustomCounter.create(this, options);
        })
    }

})(jQuery);
