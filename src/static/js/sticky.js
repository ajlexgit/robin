(function($) {

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.
        Для фикса margin-top родительскому элементу нужно задать overflow: auto.

        Требует:
            jquery.utils.js

        Параметры:
            strategy:         - метод перемещения блока ("margin" или "fixed")
            topOffset         - расстояние от верха окна до ползающего блока
            bottomOffset      - расстояние от низа родительского блока
                                до ползающего блока
     */

    var $window = $(window);
    var stickies = [];

    var capitalize = function(string) {
        return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
    };

    window.Sticky = (function() {
        var Sticky = function(block, options) {
            this.$block = $.findFirstElement(block);
            if (!this.$block.length) {
                console.error('Sticky can\'t find block');
                return
            }

            this.$container = this.$block.parent();

            // настройки
            this.opts = $.extend(true, this.getDefaultOpts(), options);

            // включение
            if (window.innerWidth >= this.opts.minEnableWidth) {
                this.enable()
            }

            // Сохраняем объект в массив для использования в событиях
            stickies.push(this);
        };

        Sticky.prototype.getDefaultOpts = function() {
            return {
                strategy: 'fixed',     // margin / fixed
                topOffset: 50,
                bottomOffset: 50,
                minEnableWidth: 768
            }
        };

        /*
            Включение ползания
         */
        Sticky.prototype.enable = function() {
            if (this.enabled) {
                return
            } else {
                this.enabled = true;
            }

            if (this.opts.strategy == 'fixed') {
                this.updateWidth();
            }
            this.process();
        };

        /*
            Выключение ползания
         */
        Sticky.prototype.disable = function() {
            if (!this.enabled) {
                return
            } else {
                this.enabled = false;
            }

            this.$block.css({
                marginTop: ''
            })
        };


        /*
            Запоминаем ширину блока (для strategy = fixed)
         */
        Sticky.prototype.updateWidth = function() {
            var initial_css = this.$block.get(0).style.cssText;
            this.$block.get(0).style.cssText = '';

            this._width = this.$block.width();
            this.$block.get(0).style.cssText = initial_css;

            return this._width;
        };


        /*
            Обработка скролла
         */
        Sticky.prototype.process = function(win_scroll) {
            if (!this.enabled) {
                return
            }

            var methodName = '_process' + capitalize(this.opts.strategy);
            if (methodName in this) {
                this[methodName].call(this, win_scroll);
            }
        };


        /*
            Обработка скролла при стратегии fixed
         */
        Sticky.prototype._processFixed = function(win_scroll) {
            var container_top = this.$container.offset().top + (parseInt(this.$container.css('padding-top')) || 0);
            var block_height = this.$block.outerHeight();
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
            } else if (win_scroll > scrollTo) {
                if (this._state != 'bottom') {
                    this._state = 'bottom';
                    this.$block.css({
                        position: 'absolute',
                        top: '',
                        bottom: this.opts.bottomOffset,
                        width: ''
                    });
                }
            } else {
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
        };

        /*
            Обработка скролла при стратегии margin
         */
        Sticky.prototype._processMargin = function(win_scroll) {
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

        return Sticky;
    })();

    var applyStickies = function() {
        var win_scroll = $window.scrollTop();
        $.each(stickies, function(i, obj) {
            obj.process(win_scroll);
        });
    };

    $window.on('scroll.sticky', applyStickies);
    $window.on('load.sticky', applyStickies);
    $window.on('resize.sticky', $.rared(function() {
        $.each(stickies, function() {
            if (window.innerWidth < this.opts.minEnableWidth) {
                this.disable()
            } else {
                this.enable()
            }
        });
    }, 100));

})(jQuery);
