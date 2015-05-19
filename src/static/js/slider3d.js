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

        var prepare_right_scroll = function() {
            var $next = that.get_next();
            if (!$next || !$next.length) {
                return;
            };
            return $next.addClass('right');
        };
        
        // Скролл вправо
        that.slide_right = function() {
            var $next = prepare_right_scroll();
            if (!$next) return;

            $wrapper.css({
                transitionDuration: settings.speed + 'ms'
            }).addClass('rotate-right').one(transitionend, function() {
                $front.removeClass('front');
                $front = $next.removeClass('right').addClass('front');
                $wrapper.removeAttr('style').removeClass('rotate-right');
            });
        };

        var prepare_left_scroll = function() {
            var $prev = that.get_prev();
            if (!$prev || !$prev.length) {
                return;
            };
            return $prev.addClass('left');
        };
        
        // Скролл влево
        that.slide_left = function () {
            var $prev = prepare_left_scroll();
            if (!$prev) return;

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
        };
        
        // Touch
        $root.on('touchstart MSPointerDown pointerdown', function(event) {
            var orig = event.originalEvent;
            var touchPoints = (typeof orig.changedTouches != 'undefined') ? orig.changedTouches : [orig];
            var touch = touchPoints[0];

            that.direction = null;
            that.scroll2deg = Math.round($wrapper.outerWidth() / 180);
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
                var angle = 0;
                
                if (diff_x < 0) {
                    // скролл вправо
                    if (that.direction != 'right') {
                        that.direction = 'right';
                        var $next = prepare_right_scroll();
                        if (!$next) return;
                    };
                    
                    angle = Math.round((diff_x + settings.prevent_scroll) / that.scroll2deg);
                } else {
                    // скролл влево
                    if (that.direction != 'left') {
                        that.direction = 'left';
                        var $prev = prepare_left_scroll();
                        if (!$prev) return;
                    };
                    
                    angle = Math.round((diff_x - settings.prevent_scroll) / that.scroll2deg);
                }
                
                $.animation_frame(function() {
                    $wrapper.css({
                        transform: 'translate3d(0, 0, -0.5em) rotateY(' + angle + 'deg)'
                    });
                }, $wrapper.get(0))();
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