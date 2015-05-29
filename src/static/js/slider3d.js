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

        that.angle = 0;
        that.initial_angle = 0;
        that.scroll2deg = 1;
        
        // Обновление глубины
        that.update_depth = function() {
            $root.css({
                perspective: $wrapper.outerWidth(),
                fontSize: $front.outerWidth()
            });
        };

        // Получение следующего слайда
        that.getNext = function() {
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
        that.getPrev = function() {
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

        var slideByAngle = function(angle) {
            return angle < 0 ? Math.ceil(-angle / 90) : Math.floor(-angle / 90);
        };
        
        // ==============
        // === DRAGER ===
        // ==============
        that.drager = new Drager($root, {
            momentumWeight: 500,
            onStartDrag: function() {
                that.angle = that.angle % 360;
                that.initial_angle = that.angle;
                that.scroll2deg = Math.round($wrapper.outerWidth() / 180);
            },
            onDrag: function(evt) {
                var absDx = Math.abs(evt.dx);
                var absDy = Math.abs(evt.dy);

                // Блокировка вертикального скролла
                if (absDy < (absDx * 3)) {
                    evt.origEvent.preventDefault();
                }

                var currentSlideIndex = slideByAngle(that.angle);
                var dAngle = Math.round(evt.dx / that.scroll2deg);
                that.angle = that.initial_angle + dAngle;
                var nextSlideIndex = slideByAngle(that.angle);
                
                // Показ соседнего слайда
                if (nextSlideIndex > currentSlideIndex) {
                    // крутим вправо
                    // TODO: no next, no prev
                    var $next = that.getNext();
                    var $prev = that.getPrev();
                    if (nextSlideIndex > 1) {
                        that.initial_angle += 90;
                        that.angle += 90;
                        
                        $prev.removeClass('left');
                        $front.removeClass('front').addClass('left');
                        $front = $next.removeClass('right').addClass('front');
                        $next = that.getNext();
                        $next.addClass('right');
                    } else {
                        $next.addClass('right');
                    }
                } else if (nextSlideIndex < currentSlideIndex) {
                    // крутим влево
                    // TODO: no next, no prev
                    var $next = that.getNext();
                    var $prev = that.getPrev();
                    if (nextSlideIndex < -1) {
                        $next.removeClass('right');
                        $front.removeClass('front').addClass('right');
                        $front = $prev.removeClass('left').addClass('front');
                        that.initial_angle -= 90;
                        that.angle -= 90;
                        $prev = that.getPrev();
                    }
                    $prev.addClass('left');
                }
                
                $.animation_frame(function() {
                    $wrapper.css({
                        transform: 'translate3d(0, 0, -0.5em) rotateY(' + that.angle + 'deg)'
                    });
                }, $wrapper.get(0))();
            },
            onStopDrag: function(evt) {
                // Ограничение скорости
                evt.setMomentumSpeed(
                    Math.max(-settings.maxMomentumSpeed, Math.min(settings.maxMomentumSpeed, evt.momentum.speedX)),
                    Math.max(-settings.maxMomentumSpeed, Math.min(settings.maxMomentumSpeed, evt.momentum.speedY))
                );
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
            maxMomentumSpeed: 1,
            controls: true,
            controlsParent: null
        }, options);

        return this.each(function() {
            var $slider = $(this);
            var object = new Slider3D($slider, settings);
            $slider.data('slider', object);
        });
    };

})(jQuery);