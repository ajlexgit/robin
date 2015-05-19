(function($) {

    var transitionend = 'transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd';

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
                transitionDuration: settings.speed + 'ms'
            }).addClass('rotate-right').one(transitionend, function() {
                $front.removeClass('front');
                $front = $next.removeClass('right').addClass('front');
                $wrapper.removeAttr('style').removeClass('rotate-right');
            });
        };

        // Скролл влево
        that.slide_left = function () {
            var $prev = that.get_prev();
            if (!$prev || !$prev.length) {
                return;
            }

            $prev.addClass('left');

            $wrapper.css({
                transitionDuration: settings.speed + 'ms'
            }).addClass('rotate-left').one(transitionend, function () {
                $front.removeClass('front');
                $front = $prev.removeClass('left').addClass('front');
                $wrapper.removeAttr('style').removeClass('rotate-left');
            });
        };

        // Инициализация
        that.update_depth();
        
        if (settings.controls) {
            var controls_parent;
            if (typeof settings.controlsParent == 'string') {
                controls_parent = $(settings.controlsParent);
            } else if (settings.controlsParent) {
                controls_parent = settings.controlsParent;
            } else {
                controls_parent = $root;
            }
            
            var $left = $('<div>').addClass('arrow arrow-left').on('click', function() {
                that.slide_left();
            });
            var $right = $('<div>').addClass('arrow arrow-right').on('click', function() {
                that.slide_right();
            });
            controls_parent.first().append($left, $right);
        }
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
            speed: 1000,
            controls: true,
            controlsParent: null
        }, options);

        return this.each(function() {
            var $slider = $(this);
            var object = new Slider3d($slider, settings);
            $slider.data('slider', object);
        });
    };

})(jQuery);