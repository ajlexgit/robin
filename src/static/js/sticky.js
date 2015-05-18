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
    */

    var userAgent = window.navigator.userAgent.toLowerCase(),
        ios = /iphone|ipod|ipad/.test(userAgent);

    var enabled = false;
    var stickies = [];
    var $window = $(window);

    $.sticky = {
        min_width: 768
    };

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
    enabled = window.innerWidth >= $.sticky.min_width;
    if (enabled) {
        $(document).on('scroll.sticky', _scrollHandler).on('mousewheel.sticky', scrollHandler);
        $window.on('load.sticky', scrollHandler);
    }

    $window.on('resize.sticky', $.rared(function() {
        $.each(stickies, function(index, sticky) {
            resetWidth(sticky.$block);
            processSticky(sticky);
        });

        // Отключаем на мобилах
        if (enabled && (window.innerWidth < $.sticky.min_width)) {
            enabled = false;
            $(document).off('.sticky');
            $window.off('load.sticky');

            $.each(stickies, function (index, sticky) {
                sticky.$block.css({
                    position: 'static',
                    width: ''
                });
            });
        } else if (!enabled && (window.innerWidth >= $.sticky.min_width)) {
            enabled = true;
            $(document).on('scroll.sticky', _scrollHandler).on('mousewheel.sticky', scrollHandler);
            $window.on('load.sticky', scrollHandler);
        }
    }, 50));

    $.fn.sticky = function(options) {
        var settings = $.extend({
            windowTopOffset: 0,
            containerBottomOffset: 0
        }, options);

        return this.each(function() {
            var sticky = {
                $block: $(this).addClass('pix-sticky'),
                windowTopOffset: settings.windowTopOffset,
                containerBottomOffset: settings.containerBottomOffset
            };
            processSticky(sticky);
            stickies.push(sticky);
        });
    }

})(jQuery);