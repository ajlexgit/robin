(function($) {

    window.SliderControlsPlugin = (function(parent) {
        var SliderControlsPlugin = function(settings) {
            parent.call(this, settings);
        };

        var _ = function() { this.constructor = SliderControlsPlugin; };
        _.prototype = parent.prototype;
        SliderControlsPlugin.prototype = new _;


        SliderControlsPlugin.prototype.getDefaultOpts = function() {
            return {
                speed: 300,
                easing: 'ease-in',
                container: null
            };
        };

        SliderControlsPlugin.prototype.init = function(slider) {
            parent.prototype.init.call(this, slider);

            // Добавление стрелок
            var $container = this.getContainer(slider);
            if ($container.length) {
                $container = $container.first();
                slider.controls = this.createControls(slider, $container);
            }
        };

        // Метод, возвращающий контейнер, куда будут добавлены стрелки
        SliderControlsPlugin.prototype.getContainer = function(slider) {
            if (this.opts.container) {
                var $container = $(this.opts.container);
            } else {
                $container = slider.$root
            }
            return $container;
        };

        // Метод, добавляющий стрелки
        SliderControlsPlugin.prototype.createControls = function(slider, $container) {
            var that = this;

            var $left = $('<div>')
                .addClass('slider-arrow slider-arrow-left')
                .appendTo($container)
                .on('click', function() {
                    that.slideLeft(slider);
                });

            var $right = $('<div>')
                .addClass('slider-arrow slider-arrow-right')
                .appendTo($container)
                .on('click', function() {
                    that.slideRight(slider);
                });

            return {
                left: $left,
                right: $right
            };
        };

        // Скролл к следующему слайду
        SliderControlsPlugin.prototype.slideRight = function(slider) {
            var $curr = slider.$currentSlide;
            var $next = slider.getNextSlide($curr);
            if (!$next || !$next.length) {
                return
            }

            // можно ли крутить
            if (this.canSlideRight(slider, $curr, $next) === false) {
                return
            }

            this.processSlideRight(slider, $curr, $next);
        };


        // Подготовка текущего слайда
        SliderControlsPlugin.prototype.canSlideRight = function(slider, $currentSlide, $nextSlide) {
            if ($currentSlide._animation) {
                return false
            }
        };

        // Подготовка текущего слайда
        SliderControlsPlugin.prototype.processSlideRight = function(slider, $currentSlide, $nextSlide) {
            $currentSlide.css({
                zIndex: 5
            });
            $nextSlide.css({
                left: '100%',
                zIndex: 10
            });

            slider.$currentSlide = $nextSlide;

            $currentSlide._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($currentSlide.get(0).style.left);
                    this.diff = -100 - this.initial;
                },
                step: function(eProgress) {
                    $currentSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $currentSlide._animation = null;
                }
            });

            $nextSlide._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($nextSlide.get(0).style.left);
                    this.diff = -this.initial;
                },
                step: function(eProgress) {
                    $nextSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $nextSlide._animation = null;
                }
            });
        };


        // Скролл к следующему слайду
        SliderControlsPlugin.prototype.slideLeft = function(slider) {
            var $curr = slider.$currentSlide;
            var $prev = slider.getPreviousSlide($curr);
            if (!$prev || !$prev.length) {
                return
            }

            // можно ли крутить
            if (this.canSlideLeft(slider, $curr, $prev) === false) {
                return
            }

            this.processSlideLeft(slider, $curr, $prev);
        };


        // Подготовка текущего слайда
        SliderControlsPlugin.prototype.canSlideLeft = function(slider, $currentSlide) {
            if ($currentSlide._animation) {
                return false
            }
        };

        // Подготовка текущего слайда
        SliderControlsPlugin.prototype.processSlideLeft = function(slider, $currentSlide, $previousSlide) {
            $currentSlide.css({
                zIndex: 5
            });
            $previousSlide.css({
                left: '-100%',
                zIndex: 10
            });

            slider.$currentSlide = $previousSlide;

            $currentSlide._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($currentSlide.get(0).style.left);
                    this.diff = 100 - this.initial;
                },
                step: function(eProgress) {
                    $currentSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $currentSlide._animation = null;
                }
            });

            $previousSlide._animation = $.animate({
                duration: this.opts.speed,
                init: function() {
                    this.initial = parseInt($previousSlide.get(0).style.left);
                    this.diff = -this.initial;
                },
                step: function(eProgress) {
                    $previousSlide.css('left', this.initial + this.diff * eProgress + '%');
                },
                complete: function() {
                    $previousSlide._animation = null;
                }
            });
        };

        return SliderControlsPlugin;
    })(SliderPlugin);

})(jQuery);
