(function($) {

    var Slider3d = function($root, settings) {
        var that = this;
        var $wrapper = $root.find('.slider3d-wrapper:first');
        var base_wrapper_transform = $wrapper.css('transform');
        var $front = $root.find('.front:first');

        // Обновление глубины
        that.update_depth = function() {
            $root.css({
                perspective: $wrapper.outerWidth(),
                fontSize: $front.outerWidth()
            });
        };

        // Получение следующего слайда
        that.get_next = function() {
            var $next = $front.next();
            if (!$next.length) {
                $next = $front.parent().children().first();
            }
            if ($next.hasClass('front')) {
                console.error('Need more slides!');
                return
            }
            return $next;
        };

        // Получение предыдущего слайда
        that.get_prev = function() {
            var $prev = $front.prev();
            if (!$prev.length) {
                $prev = $front.parent().children().last();
            }
            if ($prev.hasClass('front')) {
                console.error('Need more slides!');
                return
            }
            return $prev;
        };

        // Скролл вправо
        that.slide_right = function() {
            var $next = that.get_next();
            if (!$next || !$next.length) {
                return;
            }

            $next.addClass('right');

            $wrapper.css({
                transition: 'transform ' + settings.speed + 'ms linear'
            }).addClass('rotate-right');

            that.timer = setTimeout(function() {
                $front.removeClass('front');
                $front = $next.removeClass('right').addClass('front');
                $wrapper.removeAttr('style').removeClass('rotate-right');
            }, settings.speed);
        };

        // Скролл влево
        that.slide_left = function () {
            var $prev = that.get_prev();
            if (!$prev || !$prev.length) {
                return;
            }

            $prev.addClass('left');

            $wrapper.css({
                transition: 'transform ' + settings.speed + 'ms linear'
            }).addClass('rotate-left');

            that.timer = setTimeout(function () {
                $front.removeClass('front');
                $front = $prev.removeClass('left').addClass('front');
                $wrapper.removeAttr('style').removeClass('rotate-left');
            }, settings.speed);
        };

        // Инициализация
        that.update_depth();
    };

    $(window).on('resize', $.rared(function() {
        $('.slider3d').each(function() {
            var slider = $(this).data('slider');
            if (slider) {
                slider.update_depth();
            }
        });
    }, 50));

    $.fn.slider3d = function(options) {
        var settings = $.extend({
            speed: 1000
        }, options);

        return this.each(function() {
            var $slider = $(this);
            var object = new Slider3d($slider, settings);
            $slider.data('slider', object);
        });
    };

})(jQuery);