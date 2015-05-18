(function($) {

    /*

        Плагин, устанавливающий высоту элемента равной высоте окна,
        при условии, что позволяет высота содержимого.

        Требует:
            rared.js

        Пример:
            $.winHeight('.block');      - разовая установка высоты
            $('.block').winHeight();    - обновляемая высота

    */

    var winBlocks = [];
    var $window = $(window);

    $.winHeight = function($blocks) {
        var win_height = document.documentElement.clientHeight;

        if (!$blocks.jquery) {
            $blocks = $($blocks);
        }

        return $blocks.each(function () {
            var $block = $(this).height('auto');
            var block_height = $block.outerHeight();
            $block.outerHeight(Math.max(block_height, win_height));
        })
    };

    // Обновление высот блоков при ресайзе
    $window.on('resize.winHeight', $.rared(function() {
        $.each(winBlocks, function(index, winBlock) {
            $.winHeight(winBlock.$block);
        });
    }, 50));

    $.fn.winHeight = function() {
        return this.each(function () {
            var $block = $(this).addClass('win-height-block');

            var winBlock = {
                block: $block
            };
            $.winHeight($block);
            winBlocks.push(winBlock);
        });
    };

})(jQuery);