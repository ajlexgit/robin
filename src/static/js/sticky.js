(function($) {

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.
        Для фикса margin-top родительскому элементу нужно задать overflow: auto.

        Требует:
            jquery.utils.js, media_inspector.js

        Параметры:
            strategy          - метод перемещения блока ("margin" или "fixed")
            topOffset         - расстояние от верха окна до ползающего блока
            bottomOffset      - расстояние от низа родительского блока до ползающего блока
            minEnabledWidth   - минимальная ширина экрана, при которой блок перемещается

        Пример:
            $('.block').sticky()

     */

    var $window = $(window);
    var stickies = [];

    var capitalize = function(string) {
        return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
    };


    window.Sticky = Class(null, function Sticky(cls, superclass) {
        cls.dataParamName = 'sticky';

        cls.init = function(block, options) {
            this.$block = $(block).first();
            if (!this.$block.length) {
                return this.raise('block not found');
            }

            // настройки
            this.opts = $.extend({
                strategy: 'fixed',
                topOffset: 0,
                bottomOffset: 0,
                minEnabledWidth: 768
            }, options);

            if ((this.opts.strategy != 'margin') && (this.opts.strategy != 'fixed')) {
                return this.raise('undefined strategy');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$block.data(this.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // родительский контейнер
            this.$container = this.$block.parent();

            // Включение и выключение ползания в зависимости
            // от ширины окна браузера
            var that = this;
            $.mediaInspector.inspect(this.$block, {
                point: that.opts.minEnabledWidth,
                afterCheck: function($block, opts, state) {
                    var old_state = this.getState($block);
                    if (state === old_state) {
                        return
                    }

                    if (state) {
                        that.enable();
                    } else {
                        that.disable()
                    }
                }
            });

            // Сохраняем объект в массив для использования в событиях
            stickies.push(this);

            this.$block.data(this.dataParamName, this);

            $.mediaInspector.check(this.$block);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.disable();
            $.mediaInspector.ignore(this.$block);
            this.$block.removeData(this.dataParamName);

            var index = stickies.indexOf(this);
            if (index >= 0) {
                stickies.splice(index, 1);
            }
        };

        /*
            Включение ползания
         */
        cls.enable = function() {
            this.updateWidth();

            if (this._enabled) {
                return
            } else {
                this._enabled = true;
            }

            this.process();
        };

        /*
            Выключение ползания
         */
        cls.disable = function() {
            if (!this._enabled) {
                return
            } else {
                this._enabled = false;
            }

            this._state = null;

            if (this.opts.strategy == 'fixed') {
                this.$block.css({
                    position: '',
                    top: '',
                    bottom: '',
                    width: ''
                });
            } else {
                this.$block.css({
                    marginTop: ''
                })
            }
        };

        /*
            Запоминаем ширину блока (для strategy = fixed)
         */
        cls.updateWidth = function() {
            if (this.opts.strategy != 'fixed') {
                return ''
            }

            var initial_css = this.$block.get(0).style.cssText;
            this.$block.get(0).style.cssText = '';

            this._width = this.$block.width();
            this.$block.get(0).style.cssText = initial_css;

            if ((this._state == 'bottom') || (this._state == 'middle')) {
                this.$block.css('width', this._width);
            }

            return this._width;
        };

        /*
            Обработка скролла
         */
        cls.process = function(win_scroll) {
            if (!this._enabled) {
                return
            }

            var methodName = '_process' + capitalize(this.opts.strategy);
            if (methodName in this) {
                this[methodName].call(this, win_scroll || $window.scrollTop());
            }
        };

        /*
            Обработка скролла при стратегии fixed
         */
        cls._processFixed = function(win_scroll) {
            var container_top = this.$container.offset().top + (parseInt(this.$container.css('padding-top')) || 0);
            var block_height = this.$block.outerHeight(true);
            var container_height = this.$container.height();
            var scrollFrom = container_top - this.opts.topOffset;
            var scrollTo = scrollFrom + container_height - block_height - this.opts.bottomOffset;

            if (win_scroll < scrollFrom) {
                if (this._state != 'top') {
                    this._state = 'top';

                    this.$block.css({
                        position: '',
                        top: '',
                        bottom: '',
                        width: ''
                    });
                }
            } else if (this.$container.height() > this.$block.outerHeight(true)) {
                if (win_scroll > scrollTo) {
                    if (this._state != 'bottom') {
                        this._state = 'bottom';
                        this.$block.css({
                            position: 'absolute',
                            top: 'auto',
                            bottom: this.opts.bottomOffset,
                            width: this._width
                        });
                    }
                } else if ((win_scroll >= scrollFrom) && (win_scroll <= scrollTo)) {
                    if (this._state != 'middle') {
                        this._state = 'middle';

                        this.$block.css({
                            position: 'fixed',
                            top: this.opts.topOffset,
                            bottom: 'auto',
                            width: this._width
                        });
                    }
                }
            }
        };

        /*
            Обработка скролла при стратегии margin
         */
        cls._processMargin = function(win_scroll) {
            var container_top = this.$container.offset().top + (parseInt(this.$container.css('padding-top')) || 0);
            var block_height = this.$block.outerHeight();
            var container_height = this.$container.height();
            var scrollFrom = container_top - this.opts.topOffset;
            var scrollTo = scrollFrom + container_height - block_height - this.opts.bottomOffset;

            if (win_scroll < scrollFrom) {
                if (this._state != 'top') {
                    this._state = 'top';
                    this.$block.css({
                        marginTop: ''
                    });
                }
            } else if (win_scroll > scrollTo) {
                if (this._state != 'bottom') {
                    this._state = 'bottom';
                    this.$block.css({
                        marginTop: scrollTo - scrollFrom
                    });
                }
            } else {
                if (this._state != 'middle') {
                    this._state = 'middle';
                }

                var offset = win_scroll - scrollFrom;
                this.$block.css({
                    marginTop: offset
                });
            }
        };
    });


    var applyStickies = function() {
        var win_scroll = $window.scrollTop();
        $.each(stickies, function(i, item) {
            $.animation_frame(function() {
                item.process(win_scroll);
            })(item.$block.get(0));
        });
    };

    $window.on('scroll.sticky', applyStickies);
    $window.on('load.sticky', applyStickies);

    $.fn.sticky = function(options) {
        return this.each(function() {
            Sticky(this, options);
        })
    }

})(jQuery);
