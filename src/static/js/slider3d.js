(function($) {

    /*
        Плагин 3D-слайдера.

        Требует:
            jquery.drager.js, jquery.rared.js, jquery.animation_frame.js
    */

    var transitionend = 'transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd';

    var Slider3D = function($root, settings) {
        var that = this;
        var $empty = $();
        var $wrapper = $root.find('.slider3d-wrapper:first');
        var enabled = false;
        var items = {
            first: $empty,
            last: $empty,
            left: $empty,
            front: $empty,
            right: $empty
        }
        
        that.angle = 0;
        that.initial_angle = 0;
        that.scroll2deg = 1;
        
        // Обновление глубины
        that.update_depth = function() {
            $root.css({
                perspective: $wrapper.outerWidth(),
                fontSize: items.front.outerWidth()
            });
        };
        
        // Обновление параметров слайдера
        that.refresh = function() {
            var $slides = $root.find('.slide');
            items.first = $slides.first();
            items.last = $slides.last();
            
            if (items.first.length) {
                that.update_depth();
                enabled = items.first.get(0) != items.last.get(0);
            }
        };
        
        // Получение следующего слайда
        var getNext = function($item) {
            if ($item.get(0) == items.last.get(0)) {
                return items.first
            } else {
                return $item.next()
            }
        };

        // Получение предыдущего слайда
        var getPrev = function($item) {
            if ($item.get(0) == items.first.get(0)) {
                return items.last
            } else {
                return $item.prev()
            }
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

                var oldAngle = that.angle;
                var dAngle = Math.round(evt.dx / that.scroll2deg);
                that.angle = that.initial_angle + dAngle;
                var fromSlide = oldAngle > 0 ? Math.floor(-oldAngle / 90) : Math.ceil(-oldAngle / 90);
                var toSlide = that.angle > 0 ? Math.floor(-that.angle / 90) : Math.ceil(-that.angle / 90);
                
                if (dAngle < 0) {
                    // крутим вправо
                    if (toSlide == 1) {
                        items.right.addClass('right');
                    } else if (toSlide > 1) {
                        that.angle += (toSlide - 1) * 90;
                        that.initial_angle += (toSlide - 1) * 90;
                        
                        items.left.removeClass('left');
                        items.front.removeClass('front');
                        items.right.removeClass('right');
                        
                        items.left = items.front;
                        for(var i=2; i<toSlide; i++) {
                            items.left = getNext(items.left);
                        }
                        items.front = getNext(items.left).addClass('front');
                        items.right = getNext(items.front).addClass('right');
                    }
                } else {
                    // крутим влево
                    if (toSlide == -1) {
                        items.left.addClass('left');
                    } else if (toSlide < -1) {
                        that.angle += (toSlide + 1) * 90;
                        that.initial_angle += (toSlide + 1) * 90;
                        
                        items.left.removeClass('left');
                        items.front.removeClass('front');
                        items.right.removeClass('right');
                        
                        items.right = items.front;
                        for(var i=-2; i>toSlide; i--) {
                            items.right = getPrev(items.right);
                        }
                        items.front = getPrev(items.right).addClass('front');
                        items.left = getPrev(items.front).addClass('left');
                    }
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
                
                evt.setMomentumDuration(5000);
            }
        });

        // Определение элементов
        items.front = $root.find('.front:first');
        if (!items.front.length) {
            items.front = items.first.addClass('front');
        };
        
        that.refresh();
        
        items.left = getPrev(items.front);
        items.right = getNext(items.front);
        
        // Стрелки управления
        if (settings.controls) {
            var $controlsParent;
            if (typeof settings.controlsParent == 'string') {
                $controlsParent = $(settings.controlsParent).first();
            } else if (settings.controlsParent) {
                $controlsParent = settings.controlsParent.firat();
            } else {
                $controlsParent = $root;
            }

            var $left = $('<div>').addClass('arrow arrow-left').on('click', function() {
                that.drager.stopMomentumAnimation();
                
            });
            var $right = $('<div>').addClass('arrow arrow-right').on('click', function() {
                that.drager.stopMomentumAnimation();
                
            });
            $controlsParent.append($left, $right);
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
            maxMomentumSpeed: 2,
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