(function() {

    /*
        Параллакс-эффект для блока.
        Блок должен иметь position, отличный от static.

        Требует:
            rared.js, jquery.mousewheel.js, animation_frame.js

        <div id="block">
            <div class="parallax" style="background-image: url(../img/bg.jpg)">

            ...
        </div>


        $(document).ready(function () {
            $('#block').parallax({
                enlarge: 400,
                intensity: 0.5
            });
        });
    */

    var enabled = false;
    var parallaxImages = [];
    var $window = $(window);

    $.parallax = {
        min_width: 768
    };

    var scrollHandler = function() {
        if (!enabled) return;

        var win_scroll = $window.scrollTop();
        var win_height = document.documentElement.clientHeight;

        $.each(parallaxImages, function(index, parallaxImage) {
            var block_top = parallaxImage.block.offset().top;
            var block_height = parallaxImage.block_height;

            var start_point = block_top - win_height;
            var end_point = block_top + block_height;

            if ((win_scroll >= start_point) && (win_scroll <= end_point)) {
                var scroll_length = end_point - start_point;
                var position = (win_scroll - start_point) / scroll_length;

                var offset = position * parallaxImage.var_offset - parallaxImage.const_offset;

                parallaxImage.background.css({
                    top: Math.round(offset)
                });
            }
        });
    };

    var recalcParallax = function(parallaxImage) {
        var block_height = parallaxImage.block.outerHeight();
        var bg_height = block_height + parallaxImage.enlarge;

        var min_delta = (block_height - parallaxImage.enlarge) / 2;
        var max_delta = (block_height + parallaxImage.enlarge);
        var delta = min_delta + (max_delta - min_delta) * parallaxImage.intensity;

        parallaxImage.const_offset = bg_height - delta;
        parallaxImage.var_offset = bg_height + block_height - 2 * delta;

        parallaxImage.bg_height = bg_height;
        parallaxImage.block_height = block_height;

        parallaxImage.background.height(bg_height);
    };

    var _scrollHandler = $.rared($.animation_frame(scrollHandler), 25);

    // Подключение событий
    enabled = window.innerWidth >= $.parallax.min_width;
    if (enabled) {
        $(document).on('scroll.parallax', _scrollHandler).on('mousewheel.parallax', scrollHandler);
        $window.on('load.parallax', scrollHandler);
    }

    $window.on('resize.parallax', $.rared(function() {
        if (enabled) {
            $.each(parallaxImages, function (index, parallaxImage) {
                recalcParallax(parallaxImage);
            });

            // Отключаем на мобилах
            if (window.innerWidth < $.parallax.min_width) {
                enabled = false;
                $(document).off('.parallax');
                $window.off('load.parallax');

                $.each(parallaxImages, function (index, parallaxImage) {
                    parallaxImage.background.css({
                        top: '',
                        height: ''
                    });
                });
            }
        } else if (window.innerWidth >= $.parallax.min_width) {
            enabled = true;
            $(document).on('scroll.parallax', _scrollHandler).on('mousewheel.parallax', scrollHandler);
            $window.on('load.parallax', scrollHandler);
            scrollHandler();
        }
    }, 50));

    $.fn.parallax = function(options) {
        var settings = $.extend({
            enlarge: 400,
            intensity: 0.5
        }, options);

        return this.each(function() {
            var $block = $(this);
            var $background = $block.find('.parallax:first');
            if (!$background.length) return;

            $block.css('overflow', 'hidden');

            var parallaxImage = {
                block: $block,
                background: $background,
                enlarge: settings.enlarge,
                intensity: settings.intensity
            };
            parallaxImages.push(parallaxImage);

            if (enabled) {
                recalcParallax(parallaxImage);
            }
        });
    };

})(jQuery);