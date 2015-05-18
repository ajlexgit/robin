(function($) {

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.
        Родительский элемент должен иметь position, отличный от static.

        Требует:
            rared.js, jquery.mousewheel.js, animation_frame.js

        Параметры:
            windowTopOffset         - расстояние от верха окна до ползающего блока
            containerBottomOffset   - расстояние от низа родительского блока
                                      до ползающего блока
            condition               - функция. Если вернёт false, то блок займет
                                      положение по умолчанию
    */

    var userAgent = window.navigator.userAgent.toLowerCase(),
        ios = /iphone|ipod|ipad/.test(userAgent);

    var stickies = [];

    var winOffset = function() {
        // Значение вертикальной прокрутки страницы
        return window.pageYOffset || document.documentElement.scrollTop;
    };

    var resetWidth = function($element) {
        // Фиксируем ширину элемента
        var old_style = $element.get(0).style.cssText;

        $element.css({
            position: 'static',
            width: ''
        });

        var elem_width = $element.outerWidth();
        $element.css(old_style);
        $element.outerWidth(elem_width);
    };

    var processSticky = function(sticky) {
        // Проверка состояния прокрутки и установка стилей ползающему блоку
        var $block = sticky.$block;
        var $container = $block.parent();

        // Отмена по условию
        if (sticky.condition.call() === false) {
            $block.css({
                position: 'relative',
                top: 0,
                bottom: 'auto'
            });
            return
        }

        // верхняя граница смещения страницы
        var winTopY = $container.offset().top - sticky.windowTopOffset;

        // Нижняя граница смещения страницы
        var winBottomY = winTopY + $container.outerHeight() - $block.height() - sticky.containerBottomOffset;

        // Текущее смещение страницы
        var winCurrent = winOffset();

        winBottomY = Math.max(winTopY, winBottomY);

        if (winCurrent < winTopY) {
            // Элемент в наивысшей позиции
            if (sticky.state != 'top') {
                resetWidth($block);
                sticky.state = 'top';
            }

            $block.css({
                position: 'relative',
                top: 0,
                bottom: 'auto'
            });
        } else if (winCurrent > winBottomY) {
            // Элемент в наинизшей позиции
            if (sticky.state != 'bottom') {
                resetWidth($block);
                sticky.state = 'bottom';
            }

            $block.css({
                position: 'absolute',
                top: 'auto',
                bottom: sticky.containerBottomOffset
            });
        } else {
            // Элемент ползает
            if (sticky.state != 'middle') {
                resetWidth($block);
                sticky.state = 'middle';
            }

            if (ios) {
                $block.css({
                    position: 'absolute',
                    top: winCurrent - winTopY,
                    bottom: 'auto'
                });
            } else {
                $block.css({
                    position: 'fixed',
                    top: sticky.windowTopOffset,
                    bottom: 'auto'
                });
            }
        }
    };

    var scrollHandler = function() {
        $.each(stickies, function(index, sticky) {
            processSticky(sticky);
        });
    };

    var _scrollHandler = ios ?
        $.animation_frame(scrollHandler) :
        $.rared($.animation_frame(scrollHandler), 50);

    // Подключение событий
    $(document).on('scroll', _scrollHandler).on('mousewheel', scrollHandler);

    $(window).on('resize', $.rared(function() {
        $.each(stickies, function(index, sticky) {
            resetWidth(sticky.$block);
            processSticky(sticky);
        });
    }, 50));

    $.fn.pixSticky = function(options) {
        var settings = $.extend({
            windowTopOffset: 0,
            containerBottomOffset: 0,
            condition: $.noop()
        }, options);

        return this.each(function() {
            var sticky = {
                $block: $(this).addClass('pix-sticky'),
                condition: settings.condition,
                windowTopOffset: settings.windowTopOffset,
                containerBottomOffset: settings.containerBottomOffset
            };
            processSticky(sticky);
            stickies.push(sticky);
        });
    }

})(jQuery);