(function($) {

    /*
        Кастомное поле ввода чисел, которое подключется к обёртке над
        сттандартным полем

        Требует:
            jquery.utils.js

        Параметры:
            buttonClass      - класс, добавляемый кнопкам
            inputClass       - класс, добавляемый полю
            minValue         - минимальное значение поля
            maxValue         - максимальное значение поля
            beforeChange     - событие перед изменением значения
            afterChange      - событие после изменения значения

        Пример:
            <div class="custom-counter">
                <input type="number" value="1">
            </div>

            $('.custom-counter').counter()
    */

    window.CustomCounter = Class(null, function(cls, superclass) {
        var dataParamName = 'object';

        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('CustomCounter can\'t find root element');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$root.data(dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$root.data(dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                buttonClass: 'custom-counter-button',
                inputClass: 'custom-counter-input',
                minValue: 0,
                maxValue: 99,
                beforeChange: $.noop,
                afterChange: $.noop
            }, options);

            // поле
            this.$input = this.$root.find('input').first();
            if (!this.$input.length) {
                console.error('CustomCounter can\'t find input element');
                return false;
            }

            // кнопки
            this.$prev = $('<div>').text('-').insertBefore(this.$input);
            this.$next = $('<div>').text('+').insertAfter(this.$input);

            // вешаем классы
            this.$input.addClass(this.opts.inputClass);
            this.$prev.addClass(this.opts.buttonClass + ' decr');
            this.$next.addClass(this.opts.buttonClass + ' incr');

            if (this.$input.attr('type') == 'number') {
                this.$input.attr('min', this.opts.minValue);
                this.$input.attr('max', this.opts.maxValue);
            }

            // форматируем текущее значение
            this.value(this.value());

            var that = this;

            // уменьшение значения
            this.$prev.on('click.counter', function() {
                that.value(that.value() - 1);
                return false;
            });

            // увеличение значения
            this.$next.on('click.counter', function() {
                that.value(that.value() + 1);
                return false;
            });

            // форматирование значения при потере фокуса
            this.$input.on('blur.counter', function() {
                that.value(that.value());
            });
        };

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$root.removeData(dataParamName);
            this.$input.off('.counter');
            this.$prev.remove();
            this.$next.remove();
        };

        /*
            Получение и установка значения
         */
        cls.prototype.value = function(value) {
            var current = parseInt(this.$input.val()) || 0;

            if (value === undefined) {
                return current;
            } else {
                value = parseInt(value) || 0;
                value = Math.max(this.opts.minValue, Math.min(value, this.opts.maxValue));

                // callback
                if (value != current) {
                    if (this.opts.beforeChange.call(this, current, value) === false) {
                        return
                    }
                }

                if (String(value) != this.$input.val()) {
                    this.$input.val(value);
                    this.$input.trigger('change');
                }

                // callback
                if (value != current) {
                    this.opts.afterChange.call(this, value);
                }
            }
        };
    });


    $.fn.counter = function(options) {
        return this.each(function() {
            CustomCounter.create(this, options);
        })
    }

})(jQuery);
