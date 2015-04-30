(function($) {

    /*

        Плагин, устанавливающий высоту элемента равной высоте окна,
        при условии, что позволяет высота содержимого.

        Требует:
            jquery.delayed.js

        Пример:
            $('.block').winHeight();

    */

    // Определение высоты окна
    var winHeight = function() {
        if (window.innerHeight) {
            // all except Explorer
            return window.innerHeight;
        } else if (document.documentElement && document.documentElement.clientHeight) {
            // Explorer 6 Strict Mode
            return document.documentElement.clientHeight;
        } else if (document.body) {
            // other Explorers
            return document.body.clientHeight;
        }
    };


    // Установка высоты одного блока
    var setBlockHeight = function($block, height) {
        $block.height('auto');
        var block_height = $block.outerHeight();
        $block.outerHeight(Math.max(block_height, height));
    };


    // Обновление высот блоков при ресайзе
    $(window).on('resize.winHeight', $.rared(function() {
        var win_height = winHeight();
        $('.win-height-block').each(function() {
            setBlockHeight($(this), win_height);
        });
    }, 50));


    $.fn.winHeight = function() {
        var win_height = winHeight();
        return this.each(function() {
            var $block = $(this).addClass('win-height-block');
            setBlockHeight($block, win_height);
        });
    };

})(jQuery);