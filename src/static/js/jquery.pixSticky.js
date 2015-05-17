(function($) {

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.
        Родительский элемент должен иметь position, отличный от static.

        Требует:
            rared.js, jquery.mousewheel.js

        Параметры:
            windowTopOffset         - расстояние от верха окна до ползающего блока
            containerBottomOffset   - расстояние от низа родительского блока
                                      до ползающего блока
            condition               - функция. Если вернёт false, то блок займет
                                      положение по умолчанию
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
            settings = $element.data('settings');

        // Отмена по условию
        if (settings.condition.call() === false) {
            $element.css({
                position: 'relative',
                top: 0,
                bottom: 'auto'
            });
            return
        }

        // верхняя граница смещения страницы
        var winTopY = $container.offset().top - settings.windowTopOffset;

        // Нижняя граница смещения страницы
        var winBottomY = winTopY + $container.outerHeight() - $element.height() - settings.containerBottomOffset;

        // Текущее смещение страницы
        var winCurrent = winOffset();

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
                bottom: settings.containerBottomOffset
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
                    top: settings.windowTopOffset,
                    bottom: 'auto'
                });
            }
        }
    };

    $(document).on('scroll', $.rared(function() {
        $('.pix-sticky').each(check);
    }, 50)).on('mousewheel', function() {
        $('.pix-sticky').each(check);
    });

    $(window).on('resize', $.rared(function() {
        $('.pix-sticky').each(function() {
            resetWidth($(this));
            check.call(this);
        });
    }, 50));

    // Команды для управления ползающими блоками
    $.pixSticky = function(command) {
        if (command == 'refresh') {
            $('.pix-sticky').each(check);
        }
    };

    $.fn.pixSticky = function(options) {
        var settings = $.extend(true, {
            windowTopOffset: 0,
            containerBottomOffset: 0,
            condition: $.noop()
        }, options);

        return this.addClass('pix-sticky').data('settings', settings).each(check);
    }

})(jQuery);