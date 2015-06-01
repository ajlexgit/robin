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
        };

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

        var setAngle = function(angle) {
            that.angle = angle;
            $.animation_frame(function() {
                $wrapper.css({
                    transform: 'translate3d(0, 0, -0.5em) rotateY(' + that.angle + 'deg)'
                });
            }, $wrapper.get(0))();
        };

        var startAnimation = function(from, to, options) {
            var animationStart = $.now();
            var diff = to - from;
            that._animationTimer = setInterval(function() {
                var progress = ($.now() - animationStart) / options.duration;
                if (progress >= 1) {
                    progress = 1;
                    clearInterval(that._animationTimer);
                    that._animationTimer = null;
                }

                progress = $.easing[options.easing](progress);

                setAngle(from + diff * progress);
            }, 20);
        };

        var stopAnimation = function() {
            if (that._animationTimer) {
                clearInterval(that._animationTimer);
                that._animationTimer = null;
            }
        };

        var processRightSlide = function(angle) {
            var toSlide = angle > 0 ? Math.floor(-angle / 90) : Math.ceil(-angle / 90);

            if (toSlide == 1) {
                items.right.addClass('right');
            } else if (toSlide > 1) {
                angle += (toSlide - 1) * 90;
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
            return angle;
        };

        var processLeftSlide = function(angle) {
            var toSlide = angle > 0 ? Math.floor(-angle / 90) : Math.ceil(-angle / 90);

            if (toSlide == -1) {
                items.left.addClass('left');
            } else if (toSlide < -1) {
                angle += (toSlide + 1) * 90;
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
            return angle;
        };

        // ==============
        // === DRAGER ===
        // ==============
        that.drager = new Drager($root, {
            momentumWeight: 750,
            onStartDrag: function() {
                stopAnimation();
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

                var dAngle = Math.round(evt.dx / that.scroll2deg);
                that.angle = that.initial_angle + dAngle;

                if (dAngle < 0) {
                    // крутим вправо
                    that.angle = processRightSlide(that.angle);
                } else {
                    // крутим влево
                    that.angle = processLeftSlide(that.angle);
                }

                setAngle(that.angle);
            },
            onStopDrag: function(evt) {
                // Ограничение скорости
                evt.setMomentumSpeed(
                    Math.max(-settings.maxMomentumSpeed, Math.min(settings.maxMomentumSpeed, evt.momentum.speedX)),
                    Math.max(-settings.maxMomentumSpeed, Math.min(settings.maxMomentumSpeed, evt.momentum.speedY))
                );
            }
        });

        // Определение элементов
        items.front = $root.find('.front:first');
        if (!items.front.length) {
            items.front = items.first.addClass('front');
        }

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

            var $right = $('<div>').addClass('arrow arrow-right').on('mousedown touchstart', function() {
                if (that._animationTimer) return false;
            }).on('click', function() {
                if (that._animationTimer) return false;
                that.drager.stopMomentumAnimation();

                var finalAngle = (Math.ceil(that.angle / 90) - 1) * 90;
                var dAngle = finalAngle - that.angle;
                finalAngle = processRightSlide(finalAngle);
                that.angle = finalAngle - dAngle;
                setAngle(that.angle);

                startAnimation(that.angle, finalAngle, {
                    duration: settings.speed,
                    easing: 'linear'
                });
                return false;
            });
            var $left = $('<div>').addClass('arrow arrow-left').on('mousedown touchstart', function() {
                if (that._animationTimer) return false;
            }).on('click', function() {
                if (that._animationTimer) return false;
                that.drager.stopMomentumAnimation();

                var finalAngle = (Math.floor(that.angle / 90) + 1) * 90;
                var dAngle = finalAngle - that.angle;
                finalAngle = processLeftSlide(finalAngle);
                that.angle = finalAngle - dAngle;
                setAngle(that.angle);

                startAnimation(that.angle, finalAngle, {
                    duration: settings.speed,
                    easing: 'linear'
                });
                return false;
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