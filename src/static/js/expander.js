(function() {

    /*
        Сворачивание / разворачивание блока, представленного в двух версиях.

        Требует:
            jquery.utils.js

        Параметры:
            shortBlockSelector  - селектор краткой версии
            fullBlockSelector   - селектор полной версии
            buttonSelector      - селектор кнопок, которые сворачиают / разворачивают блок
            hiddenClass         - класс скрытого блока
            speed               - скорость сворачивания / разворачивания
            easing              - функция сглаживания сворачивания

            onBeforeExpand      - событие перед разворачиванием блока.
                                  Если вернёт false, блок не будет развернут.
            onAfterExpand       - событие после разворачивания блока
            onBeforeReduce      - событие перед сворачиванием блока.
                                  Если вернёт false, блок не будет свернут.
            onAfterReduce       - событие после сворачивания блока

        Пример:
            <div id="text-block">
                <div class="expander-short">...</div>
                <div class="expander-full hidden">...</div>
                <a href="#" class="expander-btn">read more</a>
            </div>

            $(document).ready(function() {
                $('#text-block').expander();
            });
     */

    window.Expander = Class(null, function Expander(cls, superclass) {
        cls.prototype.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({
                shortBlockSelector: '.expander-short',
                fullBlockSelector: '.expander-full',
                buttonSelector: '.expander-btn',
                hiddenClass: 'hidden',
                speed: 400,
                easing: 'easeOutQuad',

                onBeforeExpand: $.noop,
                onAfterExpand: $.noop,
                onBeforeReduce: $.noop,
                onAfterReduce: $.noop
            }, options);

            // варианты текста
            this.$short = this.$root.find(this.opts.shortBlockSelector).first();
            if (!this.$short.length) {
                return this.raise('short block not found');
            }

            this.$full = this.$root.find(this.opts.fullBlockSelector).first();
            if (!this.$full.length) {
                return this.raise('full block not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // css
            this.$full.css('overflow', 'hidden');

            // определяем текущее состояние
            this._expanded = this.$short.hasClass(this.opts.hiddenClass);
            if (this._expanded) {
                this.$full.removeClass(this.opts.hiddenClass);
            } else {
                this.$full.addClass(this.opts.hiddenClass);
            }

            // клик на кнопки сворачивания / разворачивания
            var that = this;
            this.$root.on('click.expander', this.opts.buttonSelector, function() {
                if (that._expanded) {
                    that.reduce($(this));
                } else {
                    that.expand($(this));
                }
                return false
            });

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.$root.off('.expander');
            this.$root.removeData(cls.dataParamName);
        };

        /*
            Определение высот блоков перед сворачиванием / разворачиванием
         */
        cls.prototype._prepare_resize = function() {
            if (this.$full.hasClass(this.opts.hiddenClass)) {
                this._current_height = this.$short.height();
                this.$full.removeClass(this.opts.hiddenClass);
                this._full_height = this.$full.height();
            } else {
                this._current_height = this.$full.height();
                this.$full.height('');
                this._full_height = this.$full.height();
            }

            this.$short.removeClass(this.opts.hiddenClass);
            this._short_height = this.$short.height();
            this.$short.addClass(this.opts.hiddenClass);
        };

        /*
            Разворачивание блока
         */
        cls.prototype.expand = function($button) {
            if (this._expanded) {
                return
            }

            if (this.opts.onBeforeExpand.call(this, $button) === false) {
                return
            }

            this._expanded = true;

            this._prepare_resize();
            this.$full.height(this._current_height);

            // анимация
            var that = this;
            this.$full.stop(false, false).animate({
                height: this._full_height
            }, {
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    that.$full.height('');
                    that.opts.onAfterExpand.call(this, $button);
                }
            })
        };

        /*
            Сворачивание блока
         */
        cls.prototype.reduce = function($button) {
            if (!this._expanded) {
                return
            }

            if (this.opts.onBeforeReduce.call(this, $button) === false) {
                return
            }

            this._expanded = false;

            this._prepare_resize();
            this.$full.height(this._current_height);

            // анимация
            var that = this;
            this.$full.stop(false, false).animate({
                height: this._short_height
            }, {
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    that.$full.height('');
                    that.$full.addClass(that.opts.hiddenClass);
                    that.$short.removeClass(that.opts.hiddenClass);
                    that.opts.onAfterReduce.call(this, $button);
                }
            })
        };
    });
    Expander.dataParamName = 'expander';


    $.fn.expander = function(options) {
        return this.each(function() {
            Expander.create(this, options);
        })
    }

})(jQuery);
