(function() {

    /*
        Параллакс-эффект для блока.
        Блок должен иметь position, отличный от static.

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

    var parallaxImages = [];
    var $window = $(window);

    var scrollHandler = function() {
        // Отключаем на мобилах
        if (window.innerWidth < 768) {
            $.each(parallaxImages, function (index, parallaxImage) {
                parallaxImage.background.css({
                    top: 0
                });
            });
            return
        };

        var win_scroll = $window.scrollTop();
        var win_height = document.documentElement.clientHeight;

        $.each(parallaxImages, function(index, parallaxImage) {
            var block_top = parallaxImage.block.offset().top;
            var block_height = parallaxImage.block_height;
            var bg_height = parallaxImage.bg_height;

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
        var block_height = parallaxImage.block.height();
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

    $window.on('scroll', $.rared(function() {
        if (window.requestAnimationFrame) {
            window.requestAnimationFrame(scrollHandler);
        } else {
            scrollHandler();
        }
    }, 30)).on('resize', $.rared(function() {
        $.each(parallaxImages, function(index, parallaxImage) {
            recalcParallax(parallaxImage);
        });
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
            }
            recalcParallax(parallaxImage);
            parallaxImages.push(parallaxImage);
        });
    };

})(jQuery);