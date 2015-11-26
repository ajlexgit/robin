(function() {

    /*
        Сворачивание / разворачивание текста, представленного в двух версиях.

        Требует:
            jquery.utils.js

        Параметры:
            shortTextSelector   - селектор краткой версии текста
            fullTextSelector    - селектор полной версии текста
            buttonSelector      - селектор кнопок, которые сворачиают / разворачивают текст
            hiddenClass         - класс скрытого текста
            speed               - скорость сворачивания
            easing              - функция сглаживания сворачивания

        Пример:
            <div id="expander">
                <div class="short-text">...</div>
                <div class="full-text">...</div>
                <a href="#" class="expander">read more</a>
            </div>

            $(document).ready(function() {
                Expander.create('#expander');
            });
     */

    window.Expander = Class(null, function(cls, superclass) {
        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('Expander can\'t find root element');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$root.data(Expander.dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$root.data(Expander.dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                shortTextSelector: '.short-text',
                fullTextSelector: '.full-text',
                buttonSelector: '.expander',
                hiddenClass: 'hidden',
                speed: 500,
                easing: 'easeOutQuad',

                onBeforeExpand: $.noop,
                onAfterExpand: $.noop,
                onBeforeReduce: $.noop,
                onAfterReduce: $.noop
            }, options);

            // варианты текста
            this.$short = this.$root.find(this.opts.shortTextSelector).first();
            this.$full = this.$root.find(this.opts.fullTextSelector).first();
            if (!this.$short.length || !this.$full.length) {
                console.log('Not all text variations are found');
                return false;
            }

            this.$full.css('overflow', 'hidden');

            // текущее состояние
            this.expanded = this.$short.hasClass(this.opts.hiddenClass);
            if (this.expanded) {
                this.$full.removeClass(this.opts.hiddenClass);
            } else {
                this.$full.addClass(this.opts.hiddenClass);
            }

            // клик на кнопки сворачивания / разворачивания
            var that = this;
            this.$root.on('click.expander', this.opts.buttonSelector, function() {
                that.clickHandler($(this));
                return false
            })
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.disable();
            this.$root.removeData(Expander.dataParamName);
            this.$root.off('.expander');
        };

        /*
            Клик на кнопку сворачивания / разворачивания
         */
        cls.prototype.clickHandler = function($button) {
            var that = this;
            var from_height, to_height;

            if (this.expanded) {
                if (this.opts.onBeforeReduce.call(this, $button) === false) {
                    return
                }

                this.expanded = false;
                this.$full.height('');

                // скрываем полную версию, показываем краткую
                from_height = this.$full.height();

                // временно показываем краткую версию, чтобы найти его высоту
                this.$short.removeClass(this.opts.hiddenClass);
                to_height = this.$short.height();
                this.$short.addClass(this.opts.hiddenClass);

                // анимация
                this.$full.height(from_height);
                this.$full.stop(true, false).animate({
                    height: to_height
                }, {
                    duration: this.opts.speed,
                    easing: this.opts.easing,
                    complete: function() {
                        that.$short.removeClass(that.opts.hiddenClass);
                        that.$full.addClass(that.opts.hiddenClass);

                        that.opts.onAfterReduce.call(this, $button);
                    }
                })
            } else {
                if (this.opts.onBeforeExpand.call(this, $button) === false) {
                    return
                }

                this.expanded = true;
                this.$full.height('');

                // скрываем полную версию, показываем краткую
                from_height = this.$short.height();
                this.$short.addClass(this.opts.hiddenClass);
                this.$full.removeClass(this.opts.hiddenClass);
                to_height = this.$full.height();

                // анимация
                this.$full.height(from_height);
                this.$full.stop(true, false).animate({
                    height: to_height
                }, {
                    duration: this.opts.speed,
                    easing: this.opts.easing,
                    complete: function() {
                        that.opts.onAfterExpand.call(this, $button);
                    }
                })
            }
        };
    });
    Expander.dataParamName = 'expander';

})(jQuery);
