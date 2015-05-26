(function ($) {

    /*
        Добавляет события видимости элемента.

        Требует:
            jquery.rared.js

        Пример:
            $('#block').appear().on('appear', function() {
                $(this).addClass('visible');
            });
    */

    var appear_blocks = [];

    $.fn.appear = function(options) {
        var settings = $.extend({
            from_top: 0.2,
            from_bottom: 0.2,
            from_left: 0.2,
            from_right: 0.2
        }, options);

        return this.each(function() {
            appear_blocks.push({
                element: this,
                settings: settings
            })
        });
    };

    $.force_appear = function() {
        var vpWidth = document.documentElement.clientWidth,
            vpHeight = document.documentElement.clientHeight;

        for(var i=0, l=appear_blocks.length; i<l; i++) {
            var appear_block = appear_blocks[i],
                settings = appear_block.settings,
                rect = appear_block.element.getBoundingClientRect(),
                elem_width = rect.right - rect.left,
                elem_height = rect.bottom - rect.top,
                vDiff = Math.min(vpHeight, elem_height),
                hDiff = Math.min(vpWidth, elem_width);

            var visible = (rect.bottom >= (vDiff * settings.from_bottom));
            visible = visible && (rect.right >= (hDiff * settings.from_right));
            visible = visible && ((vpHeight - rect.top) >= (vDiff * settings.from_top));
            visible = visible && ((vpWidth - rect.left) >= (hDiff * settings.from_left));

            var $elem = $(appear_block.element);
            var old_state = $elem.data('appear-visible');
            if (old_state !== visible) {
                if (visible) $elem.trigger('appear');
                else $elem.trigger('disappear');
                $elem.data('appear-visible', visible);
            }
        }
    };

    $(document).ready(function() {
        setTimeout($.force_appear, 0);
    });

    $(window).on('scroll.appear resize.appear', $.rared($.force_appear, 50));
    $(window).on('load.appear', $.force_appear);

})(jQuery);
