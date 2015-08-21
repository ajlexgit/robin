(function($) {

    window.SliderSideAnimation = (function(parent) {
        var defaults = {
            speed: 300,
            easing: 'easeOutCubic'
        };

        // Инициализация плагина
        var SideAnimation = function(settings) {
            this.opts = $.extend(true, defaults, settings);
        };

        var _ = function() { this.constructor = SideAnimation; };
        _.prototype = parent.prototype;
        SideAnimation.prototype = new _;


        /*
            Добавление слайдеру флага анимирования для блокировки множественного нажатия
         */
        SideAnimation.prototype.onAttach = function(slider) {
            slider._animated = false;

            var transitionSpeed = (this.opts.speed / 1000).toFixed(1) + 's';
            var transition = 'height ' + transitionSpeed;
            slider.$list.css('transition', transition);
            console.log('set transition');
        };

        SideAnimation.prototype.beforeSlide = function(slider, $toSlide, instantly) {
            slider._animated = true;
        };

        SideAnimation.prototype.afterSlide = function(slider, $toSlide, instantly) {
            slider._animated = false;
        };

        /*
            Останавливаем анимацию при изменении кол-ва элементов в слайде
         */
        SideAnimation.prototype.beforeSetSlideItems = function() {
            if (this._animation) {
                this._animation.stop(true)
            }
        };

        /*
            Обеспечиваем моментальную смену высоты, когда это необходимо
         */
        SideAnimation.prototype.beforeUpdateListHeight = function(slider, instantly) {
            var current_transition = slider.$list.css('transition');
            if (instantly && current_transition && (current_transition != 'none')) {
                this._old_transition = current_transition;
                slider.$list.css('transition', 'none');
            }
        };

        SideAnimation.prototype.afterUpdateListHeight = function(slider, instantly) {
            if (instantly && this._old_transition) {
                slider.$list.css('transition', this._old_transition);
                this._old_transition = null;
            }
        };

        /*
            Реализация метода перехода от одного слайда к другому
            посредством выдвигания с края слайдера
         */
        SideAnimation.prototype.slideTo = function(slider, $toSlide) {
            if (slider._animated) {
                return
            }

            var fromIndex = slider.$slides.index(slider.$currentSlide);
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

                if (left_way < right_way) {
                    this.slideLeft(slider, $toSlide);
                } else {
                    this.slideRight(slider, $toSlide);
                }
            } else {
                if (toIndex > fromIndex) {
                    this.slideRight(slider, $toSlide);
                } else {
                    this.slideLeft(slider, $toSlide);
                }
            }
        };

        /*
            Появление нового слайда справа от текущего
         */
        SideAnimation.prototype.slideRight = function(slider, $toSlide) {
            var $fromSlide = slider.$currentSlide;

            slider.beforeSlide($toSlide);

            $toSlide.css({
                left: '100%'
            });
            slider._setCurrentSlide($toSlide);
            slider.updateListHeight();

            this._animation = $.animate({
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
                    $fromSlide.css({
                        left: ''
                    });
                    slider._animated = false;
                    slider.afterSlide($toSlide);
                }
            });
        };

        /*
            Появление нового слайда слева от текущего
         */
        SideAnimation.prototype.slideLeft = function(slider, $toSlide) {
            var $fromSlide = slider.$currentSlide;

            slider.beforeSlide($toSlide);

            $toSlide.css({
                left: '-100%'
            });
            slider._setCurrentSlide($toSlide);
            slider.updateListHeight();

            this._animation = $.animate({
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
                    $fromSlide.css({
                        left: ''
                    });
                    slider._animated = false;
                    slider.afterSlide($toSlide);
                }
            });
        };

        return SideAnimation;
    })(SliderPlugin);

})(jQuery);
