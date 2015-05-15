(function($) {

    /*

        Плагин, устанавливающий высоту элемента равной высоте окна,
        при условии, что позволяет высота содержимого.

        Требует:
            rared.js

        Пример:
            $('.block').setWinHeight();     - разовая установка высоты
            $('.block').winHeight();        - обновляемая высота

    */

    // Обновление высот блоков при ресайзе
    $(window).on('resize.winHeight', $.rared(function() {
        $('.win-height-block').setWinHeight();
    }, 50));

    // Установка высоты одного блока
    $.fn.setWinHeight = function() {
        return this.each(function() {
            var $block = $(this).height('auto');
            var block_height = $block.outerHeight();
            $block.outerHeight(Math.max(block_height, document.documentElement.clientHeight));
        })
    };

    $.fn.winHeight = function(action) {
        if (action == 'destroy') {
            return this.removeClass('win-height-block').height('');
        }

        return this.addClass('win-height-block').setWinHeight();
    };

})(jQuery);