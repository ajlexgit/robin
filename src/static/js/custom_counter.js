(function($) {

    /*
        Кастомное поле ввода чисел.

        Пример:
            <div class="custom-counter">
                <input type="text" maxlength="2" value="1">
            </div>


            $('.custom-counter').each(function() {
                CustomCounter.create(this);
            })

        Требует:
            jquery.utils.js
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
                var old_instance = this.$input.data(dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$root.data(dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                containerClass: 'custom-counter',
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
            this.$prev = $('<div>').text('-').prependTo(this.$root);
            this.$next = $('<div>').text('+').appendTo(this.$root);

            // вешаем классы
            this.$root.addClass(this.opts.containerClass);
            this.$input.addClass(this.opts.inputClass);
            this.$prev.addClass(this.opts.buttonClass + ' decr');
            this.$next.addClass(this.opts.buttonClass + ' incr');

            // форматируем текущее значение
            this.value(this.value());

            var that = this;

            // уменьшение значения
            this.$prev.on('click', function() {
                that.value(that.value() - 1);
            });

            // увеличение значения
            this.$next.on('click', function() {
                that.value(that.value() + 1);
            });

            // форматирование значения при потере фокуса
            this.$input.off('.counter').on('blur.counter', function() {
                that.value(that.value());
            });
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

        /*
            Отключение плагина
         */
        cls.prototype.destroy = function() {
            this.$root.removeData(dataParamName);
            this.$input.off('.counter');
            this.$prev.remove();
            this.$next.remove();
        };
    });

})(jQuery);
