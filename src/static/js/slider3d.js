(function($) {

    var transitionend = 'transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd';

    var Slider3d = function($root, settings) {
        var that = this;
        var $wrapper = $root.find('.slider3d-wrapper:first');
        var $front = $root.find('.front:first');
        var wrapper_data = $wrapper.data();

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

        // Подготовка к скроллу вправо
        that.before_right_scroll = function() {
            var $next = that.get_next();
            if (!$next || !$next.length) {
                return;
            }
            return $next.addClass('right');
        };

        // Скролл вправо
        that.slide_right = function() {
            var $next = that.before_right_scroll();
            if (!$next) return;

            $wrapper.removeAttr('style').css({
                transitionDuration: settings.speed + 'ms'
            }).addClass('rotate-right').one(transitionend, function() {
                $front.removeClass('front');
                $front = $next.removeClass('right').addClass('front');
                $wrapper.removeAttr('style').removeClass('rotate-right');
            });
        };

        // Подготовка к скроллу влево
        that.before_left_scroll = function() {
            var $prev = that.get_prev();
            if (!$prev || !$prev.length) {
                return;
            }
            return $prev.addClass('left');
        };

        // Скролл влево
        that.slide_left = function () {
            var $prev = that.before_left_scroll();
            if (!$prev) return;

            $wrapper.removeAttr('style').css({
                transitionDuration: settings.speed + 'ms'
            }).addClass('rotate-left').one(transitionend, function () {
                $front.removeClass('front');
                $front = $prev.removeClass('left').addClass('front');
                $wrapper.removeAttr('style').removeClass('rotate-left');
            });
        };

        // Инициализация
        that.update_depth();

        // Стрелки управления
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


        // ===============
        // ==== Touch ====
        // ===============

        // Подготовка к повороту вправо
        that.before_touchmove_right = function () {
            if (wrapper_data.direction != 'right') {
                wrapper_data.direction = 'right';
                return that.before_right_scroll();
            }
        };

        // Подготовка к повороту влево
        that.before_touchmove_left = function () {
            if (wrapper_data.direction != 'left') {
                wrapper_data.direction = 'left';
                return that.before_left_scroll();
            }
        };

        // Поворот
        that.rotate = function(diff_x) {
            wrapper_data.angle = Math.round(diff_x / wrapper_data.scroll2deg);

            $.animation_frame(function() {
                $wrapper.css({
                    transform: 'translate3d(0, 0, -0.5em) rotateY(' + wrapper_data.angle + 'deg)'
                });
            }, $wrapper.get(0))();
        };

        $root.on('touchstart MSPointerDown pointerdown', function(event) {
            var orig = event.originalEvent;
            var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
            var touch = touchPoints[0];

            wrapper_data.direction = null;
            wrapper_data.scroll2deg = Math.round($wrapper.outerWidth() / 180);

            that.touch_x = touch.pageX;
            that.touch_y = touch.pageY;
        }).on('touchmove MSPointerMove pointermove', function(event) {
            var orig = event.originalEvent;
            var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
            var touch = touchPoints[0];

            var xMovement = Math.abs(touch.pageX - that.touch_x);
            var yMovement = Math.abs(touch.pageY - that.touch_y);

            // Блокировка вертикального скролла
            if (yMovement < (xMovement * 3)) {
                event.preventDefault();
            }

            // Горизонтальный скролл
            if (xMovement > settings.prevent_scroll) {
                var diff_x = touch.pageX - that.touch_x;
                if (diff_x < 0) {
                    // скролл вправо
                    diff_x += settings.prevent_scroll;
                    that.before_touchmove_right();
                } else {
                    // скролл влево
                    diff_x -= settings.prevent_scroll;
                    that.before_touchmove_left();
                }

                that.rotate(diff_x);
            }
        })/*.on('touchend MSPointerUp pointerup', function(event) {
            var orig = event.originalEvent;
            var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
            var touch = touchPoints[0];

            console.log('dx', touch.pageX - that.touch_x);
            console.log('dy', touch.pageY - that.touch_y);
        })*/;
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
            controlsParent: null,
            prevent_scroll: 20
        }, options);

        return this.each(function() {
            var $slider = $(this);
            var object = new Slider3d($slider, settings);
            $slider.data('slider', object);
        });
    };

})(jQuery);