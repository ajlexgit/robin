(function($) {

    window.SliderSimpleAnimationPlugin = (function(parent) {
        var defaults = {
            speed: 300,
            easing: 'easeOutCubic'
        };

        // Инициализация плагина
        var SliderSimpleAnimationPlugin = function(settings) {
            this.opts = $.extend(true, defaults, settings);

            this.animations = [];
        };

        var _ = function() { this.constructor = SliderSimpleAnimationPlugin; };
        _.prototype = parent.prototype;
        SliderSimpleAnimationPlugin.prototype = new _;


        // Переопределяем метод скролла
        SliderSimpleAnimationPlugin.prototype.slide = function(slider, $fromSlide, $toSlide) {
            var fromIndex = slider.$slides.index($fromSlide);
            var toIndex = slider.$slides.index($toSlide);

            if (fromIndex == toIndex) {
                return
            }

            // определяем направление
            if (slider.opts.loop) {
                var slides_count = slider.$slides.length;

                var diff = toIndex - fromIndex;
                var right_way = diff + (diff > 0 ? 0 : slides_count);
                var left_way = (diff > 0 ? slides_count : 0) - diff;

                if (right_way < left_way) {
                    this.slideRight(slider, $fromSlide, $toSlide);
                } else {
                    this.slideLeft(slider, $fromSlide, $toSlide);
                }
            } else {
                if (toIndex > fromIndex) {
                    this.slideRight(slider, $fromSlide, $toSlide);
                } else {
                    this.slideLeft(slider, $fromSlide, $toSlide);
                }
            }
        };

        SliderSimpleAnimationPlugin.prototype.slideRight = function(slider, $fromSlide, $toSlide) {
            $fromSlide.css({
                zIndex: 5
            });
            $toSlide.css({
                left: '100%',
                zIndex: 10
            });

            slider.$currentSlide = $toSlide;

            var that = this;
            var animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.from_initial = parseInt($fromSlide.get(0).style.left);
                    this.from_diff = -100 - this.from_initial;

                    this.to_initial = parseInt($toSlide.get(0).style.left);
                    this.to_diff = -this.to_initial;
                },
                step: function(eProgress) {
                    $fromSlide.css('left', this.from_initial + this.from_diff * eProgress + '%');
                    $toSlide.css('left', this.to_initial + this.to_diff * eProgress + '%');
                },
                complete: function() {
                    $.each(that.animations, function(i, e) {
                        if (e.obj === animation) {
                            that.animations.splice(i, 1);
                            return false
                        }
                    });
                }
            });

            this.animations.push({
                from: $fromSlide,
                to: $toSlide,
                obj: animation
            });
        };

        SliderSimpleAnimationPlugin.prototype.slideLeft = function(slider, $fromSlide, $toSlide) {
            $fromSlide.css({
                zIndex: 5
            });
            $toSlide.css({
                left: '-100%',
                zIndex: 10
            });

            slider.$currentSlide = $toSlide;

            var that = this;
            var animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    this.from_initial = parseInt($fromSlide.get(0).style.left);
                    this.from_diff = 100 - this.from_initial;

                    this.to_initial = parseInt($toSlide.get(0).style.left);
                    this.to_diff = -this.to_initial;
                },
                step: function(eProgress) {
                    $fromSlide.css('left', this.from_initial + this.from_diff * eProgress + '%');
                    $toSlide.css('left', this.to_initial + this.to_diff * eProgress + '%');
                },
                complete: function() {
                    $.each(that.animations, function(i, e) {
                        if (e.obj === animation) {
                            that.animations.splice(i, 1);
                            return false
                        }
                    });
                }
            });

            this.animations.push({
                from: $fromSlide,
                to: $toSlide,
                obj: animation
            });
        };

        return SliderSimpleAnimationPlugin;
    })(SliderPlugin);

})(jQuery);
