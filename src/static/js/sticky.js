(function($) {

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.
        Для фикса margin-top родительскому элементу нужно задать overflow: auto.

        Требует:
            jquery.utils.js

        Параметры:
            topOffset         - расстояние от верха окна до ползающего блока
            bottomOffset      - расстояние от низа родительского блока
                                до ползающего блока
     */

    var $window = $(window);
    var stickies = [];

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

        Sticky.prototype.process = function(win_scroll) {
            if (!this.enabled) {
                return
            }

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
            $.animation_frame(function() {
                obj.process(win_scroll);
            })(obj.$block.get(0));
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
