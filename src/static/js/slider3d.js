(function($) {

    /*
        Плагин 3D-слайдера.

        Требует:
            jquery.drager.js, jquery.rared.js, jquery.animation_frame.js
    */

    var transitionend = 'transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd';

    var Slider3D = function($root, settings) {
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

        that.rotateTo = function(angle) {
            $.animation_frame(function() {
                wrapper_data.angle = angle;
                $wrapper.css({
                    transform: 'translate3d(0, 0, -0.5em) rotateY(' + angle + 'deg)'
                });
            }, $wrapper.get(0))();
        };

        // ==============
        // === DRAGER ===
        // ==============
        that.drager = new Drager($root, {
            deceleration: 0.06,
            speedDeceleration: 0.01,
            onStartDrag: function() {
                $wrapper.stop();
                wrapper_data.initial_angle = (wrapper_data.angle || 0) % 360;
                wrapper_data.scroll2deg = Math.round($wrapper.outerWidth() / 180);
            },
            onDrag: function(evt) {
                var absDx = Math.abs(evt.dx);
                var absDy = Math.abs(evt.dy);

                // Блокировка вертикального скролла
                if (absDy < (absDx * 3)) {
                    evt.origEvent.preventDefault();
                }

                // Горизонтальный скролл
                if (absDx > settings.prevent_scroll) {
                    var final_dx, angle;
                    if (evt.dx > 0) {
                        final_dx = evt.dx - settings.prevent_scroll;
                        that.before_left_scroll();
                    } else {
                        final_dx = evt.dx + settings.prevent_scroll;
                        that.before_right_scroll();
                    }

                    angle = Math.round(final_dx / wrapper_data.scroll2deg);
                    that.rotateTo(wrapper_data.initial_angle + angle);
                }
            },
            onStopDrag: function(evt) {
                var start_angle = wrapper_data.angle;
                $wrapper.css({
                    x: start_angle
                }).animate({
                    x: start_angle + evt.momentum.dx
                }, {
                    duration: evt.momentum.duration,
                    easing: 'easeOutCubic',
                    step: that.rotateTo
                })
            }
        });

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
            var object = new Slider3D($slider, settings);
            $slider.data('slider', object);
        });
    };

})(jQuery);