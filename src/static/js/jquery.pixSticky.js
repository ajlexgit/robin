(function($) {

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.
        Родительский элемент должен иметь position, отличный от static.

        Требует:
            jquery.mousewheel.js, rared.js
    */

    var userAgent = window.navigator.userAgent.toLowerCase(),
        ios = /iphone|ipod|ipad/.test(userAgent);

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

    var check = function() {
        // Проверка состояния прокрутки и установка стилей ползающему блоку
        var $element = $(this),
            $container = $element.parent(),
            windowTopOffset = $element.data('windowTopOffset'),
            containerBottomOffset = $element.data('containerBottomOffset'),

            // верхняя граница смещения страницы
            winTopY = $container.offset().top - windowTopOffset,

            // Нижняя граница смещения страницы
            winBottomY = winTopY + $container.outerHeight() - $element.height() - containerBottomOffset,

            // Текущее смещение страницы
            winCurrent = winOffset();

        winBottomY = Math.max(winTopY, winBottomY);

        if (winCurrent < winTopY) {
            // Элемент в наивысшей позиции
            if (this._ps_state != 'top') {
                resetWidth($element);
                this._ps_state = 'top';
            }

            $element.css({
                position: 'relative',
                top: 0,
                bottom: 'auto'
            });
        } else if (winCurrent > winBottomY) {
            // Элемент в наинизшей позиции
            if (this._ps_state != 'bottom') {
                resetWidth($element);
                this._ps_state = 'bottom';
            }

            $element.css({
                position: 'absolute',
                top: 'auto',
                bottom: containerBottomOffset
            });
        } else {
            // Элемент ползает
            if (this._ps_state != 'middle') {
                resetWidth($element);
                this._ps_state = 'middle';
            }

            if (ios) {
                $element.css({
                    position: 'absolute',
                    top: winCurrent - winTopY,
                    bottom: 'auto'
                });
            } else {
                $element.css({
                    position: 'fixed',
                    top: windowTopOffset,
                    bottom: 'auto'
                });
            }
        }
    };

    $(document).on('scroll mousewheel', $.rared(function() {
        $('.pix-sticky').each(check);
    }, 30));

    // Команды для управления ползающими блоками
    $.pixSticky = function(command) {
        if (command == 'refresh') {
            $('.pix-sticky').each(check);
        }
    };

    $.fn.pixSticky = function(options) {
        var settings = $.extend(true, {
            windowTopOffset: 0,
            containerBottomOffset: 0
        }, options);

        return this.addClass('pix-sticky').data({
            windowTopOffset: settings.windowTopOffset,
            containerBottomOffset: settings.containerBottomOffset
        }).each(check);
    }

})(jQuery);