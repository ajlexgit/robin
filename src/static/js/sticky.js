(function($) {

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.
        Для фикса margin-top родительскому элементу нужно задать overflow: auto.

        Требует:
            jquery.utils.js

        Параметры:
            strategy          - метод перемещения блока ("margin" или "fixed")
            topOffset         - расстояние от верха окна до ползающего блока
            bottomOffset      - расстояние от низа родительского блока до ползающего блока
            minEnableWidth    - минимальная ширина экрана, при которой блок перемещается

        Пример:
            $('.block').sticky()

     */

    var $window = $(window);
    var stickies = [];

    var capitalize = function(string) {
        return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
    };


    window.Sticky = Class(null, function(cls, superclass) {
        cls.init = function(block, options) {
            this.$block = $(block).first();
            if (!this.$block.length) {
                console.error('Sticky: block not found');
                return false;
            }

            // настройки
            this.opts = $.extend({
                strategy: 'fixed',
                topOffset: 0,
                bottomOffset: 0,
                minEnableWidth: 768
            }, options);

            if ((this.opts.strategy != 'margin') && (this.opts.strategy != 'fixed')) {
                console.error('Sticky: undefined strategy');
                return false;
            }

            // отвязывание старого экземпляра
            var old_instance = this.$block.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // родительский контейнер
            this.$container = this.$block.parent();

            // включение
            if (window.innerWidth >= this.opts.minEnableWidth) {
                this.enable()
            }

            // Сохраняем объект в массив для использования в событиях
            stickies.push(this);

            this.$block.data(cls.dataParamName, this);
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.disable();
            this.$block.removeData(cls.dataParamName);

            var index = stickies.indexOf(this);
            if (index >= 0) {
                stickies.splice(index, 1);
            }
        };

        /*
            Включение ползания
         */
        cls.prototype.enable = function() {
            this.updateWidth();

            if (this.enabled) {
                return
            } else {
                this.enabled = true;
            }

            this.process();
        };

        /*
            Выключение ползания
         */
        cls.prototype.disable = function() {
            if (!this.enabled) {
                return
            } else {
                this.enabled = false;
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
        cls.prototype.updateWidth = function() {
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
        cls.prototype.process = function(win_scroll) {
            if (!this.enabled) {
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
        cls.prototype._processFixed = function(win_scroll) {
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
                            top: '',
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
                            bottom: '',
                            width: this._width
                        });
                    }
                }
            }
        };

        /*
            Обработка скролла при стратегии margin
         */
        cls.prototype._processMargin = function(win_scroll) {
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
    Sticky.dataParamName = 'sticky';


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
    $window.on('resize.sticky', $.rared(function() {
        var win_scroll = $window.scrollTop();
        $.each(stickies, function() {
            if (window.innerWidth < this.opts.minEnableWidth) {
                this.disable()
            } else {
                this.enable(win_scroll)
            }
        });
    }, 100));


    $.fn.sticky = function(options) {
        return this.each(function() {
            Sticky.create(this, options);
        })
    }

})(jQuery);
