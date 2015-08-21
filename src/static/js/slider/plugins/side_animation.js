(function($) {

    window.SliderSideAnimation = (function(parent) {
        var defaults = {
            speed: 800,
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
            Реализация метода перехода от одного слайда к другому БЕЗ АНИМАЦИИ
         */
        SideAnimation.prototype.slideNowTo = function(slider, $toSlide, forceListHeight) {
            if (slider._animated) {
                return
            }

            slider.beforeSlide($toSlide, true);

            slider.$slides.css({
                left: ''
            });
            $toSlide.css({
                left: '0'
            });
            slider._setCurrentSlide($toSlide);
            slider.updateListHeight(forceListHeight);

            slider.afterSlide($toSlide, true);
        };

        /*
            Реализация метода перехода от одного слайда к другому
            посредством выдвигания с края слайдера
         */
        SideAnimation.prototype.slideTo = function(slider, $toSlide, forceListHeight) {
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
                    this.slideLeft.apply(this, arguments);
                } else {
                    this.slideRight.apply(this, arguments);
                }
            } else {
                if (toIndex > fromIndex) {
                    this.slideRight.apply(this, arguments);
                } else {
                    this.slideLeft.apply(this, arguments);
                }
            }
        };

        /*
            Появление нового слайда справа от текущего
         */
        SideAnimation.prototype.slideRight = function(slider, $toSlide, forceListHeight) {
            var $fromSlide = slider.$currentSlide;

            slider.beforeSlide($toSlide);

            $toSlide.css({
                left: '100%'
            });
            slider._setCurrentSlide($toSlide);
            slider.updateListHeight(forceListHeight);

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
                    var fromLeft = this.from_initial + this.from_diff * eProgress + '%';
                    var toLeft = this.to_initial + this.to_diff * eProgress + '%';
                    $.animation_frame(function() {
                        $fromSlide.css('left', fromLeft);
                        $toSlide.css('left', toLeft);
                    }, slider.$list.get(0))();
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
        SideAnimation.prototype.slideLeft = function(slider, $toSlide, forceListHeight) {
            var $fromSlide = slider.$currentSlide;

            slider.beforeSlide($toSlide);

            $toSlide.css({
                left: '-100%'
            });
            slider._setCurrentSlide($toSlide);
            slider.updateListHeight(forceListHeight);

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
                    var fromLeft = this.from_initial + this.from_diff * eProgress + '%';
                    var toLeft = this.to_initial + this.to_diff * eProgress + '%';
                    $.animation_frame(function() {
                        $fromSlide.css('left', fromLeft);
                        $toSlide.css('left', toLeft);
                    }, slider.$list.get(0))();
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
