(function($) {

    /*

        Плагин, устанавливающий высоту элемента равной высоте окна,
        при условии, что позволяет высота содержимого.

        Требует:
            jquery.rared.js

        Пример:
            $.winHeight('.block', 0.9);      - разовая установка высоты на 90% высоты окна
            $('.block').winHeight(0.9);      - обновляемая высота d 90% высоты окна

     */

    var winBlocks = [];
    var $window = $(window);

    $.winHeight = function($blocks, multiplier) {
        var win_height = document.documentElement.clientHeight;

        if ($.isFunction(multiplier)) {
            multiplier = multiplier() || 1;
        } else {
            multiplier = multiplier || 1;
        }

        if (!$blocks.jquery) {
            $blocks = $($blocks);
        }

        return $blocks.each(function() {
            var $block = $(this).height('auto');
            var block_height = $block.outerHeight();
            var final_height = Math.round(win_height * multiplier);
            $block.outerHeight(Math.max(block_height, final_height));
        })
    };

    // Обновление высот блоков при ресайзе
    $window.on('resize.winHeight', $.rared(function() {
        $.each(winBlocks, function(index, winBlock) {
            $.winHeight(winBlock.$block, winBlock.multiplier);
        });
    }, 50));

    $.fn.winHeight = function(multiplier) {
        return this.each(function() {
            var $block = $(this);

            var winBlock = {
                $block: $block,
                multiplier: multiplier
            };
            winBlocks.push(winBlock);

            $.winHeight($block, multiplier);
        });
    };

})(jQuery);
