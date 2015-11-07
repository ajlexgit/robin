(function($) {

    window.SliderSideAnimation = Class(SliderPlugin, function(cls, superclass) {
        // Настройки по умолчанию
        cls.prototype.getDefaultOpts = function() {
            return {
                name: 'side',
                speed: 800,
                showIntermediate: true,
                slideMarginPercent: 0,
                easing: 'easeOutCubic'
            };
        };

        /*
            Реализация метода перехода от одного слайда к другому
            посредством выдвигания с края слайдера
         */
        cls.prototype.slideTo = function(slider, $toSlide, animatedHeight) {
            if (slider._animated) {
                return
            }

            var slide_info = {
                fromIndex: slider.$slides.index(slider.$currentSlide),
                toIndex: slider.$slides.index($toSlide)
            };

            // тот же слайд?
            if (slide_info.fromIndex == slide_info.toIndex) {
                return
            }

            this.chooseSlideDirection(slider, $toSlide, animatedHeight, slide_info);
        };

        /*
            Выбор направления анимации
         */
        cls.prototype.chooseSlideDirection = function(slider, $toSlide, animatedHeight, slide_info) {
            var diff = slide_info.toIndex - slide_info.fromIndex;

            if (slide_info.toIndex > slide_info.fromIndex) {
                slide_info.count = diff;
                this.slideRight.call(this, slider, $toSlide, animatedHeight, slide_info);
            } else {
                slide_info.count = -diff;
                this.slideLeft.call(this, slider, $toSlide, animatedHeight, slide_info);
            }
        };

        /*
            Появление нового слайда справа от текущего
         */
        cls.prototype.slideRight = function(slider, $toSlide, animatedHeight, slide_info) {
            var animations = [];
            var animatedSlides = [];
            var slide_left = 100 + this.opts.slideMarginPercent;

            slider.beforeSlide($toSlide);

            // определяем слайды, учавствующие в анимации
            if (this.opts.showIntermediate) {
                var i = 0;
                var $slide = slider.$currentSlide;
                while ($slide.length && (i++ <= slide_info.count)) {
                    animatedSlides.push($slide);

                    $slide = slider.getNextSlide($slide);
                }
            } else {
                animatedSlides.push(slider.$currentSlide);
                animatedSlides.push($toSlide);
            }

            // заполнение данных о анимации каждого слайда
            var animatedSlidesCount = animatedSlides.length;
            for (i = 0; i < animatedSlidesCount; i++) {
                var $animatedSlide = animatedSlides[i];

                var left = i * slide_left;
                $animatedSlide.css({
                    left: left + '%'
                });
                animations.push({
                    $animatedSlide: $animatedSlide,
                    from_left: left,
                    to_left: left - ((animatedSlidesCount - 1) * slide_left)
                });
            }

            slider.setCurrentSlide($toSlide);

            slider._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        this.autoInit('slide_' + i, animation_data.from_left, animation_data.to_left);
                    }
                },
                step: function(eProgress) {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        animation_data.$animatedSlide.css({
                            left: this.autoCalc('slide_' + i, eProgress) + '%'
                        })
                    }
                },
                complete: function() {
                    for (var i = 0; i < (animations.length - 1); i++) {
                        var animation_data = animations[i];
                        animation_data.$animatedSlide.css({
                            left: ''
                        })
                    }
                    slider.afterSlide($toSlide);
                }
            });

            slider.updateListHeight(animatedHeight);
        };

        /*
            Появление нового слайда слева от текущего
         */
        cls.prototype.slideLeft = function(slider, $toSlide, animatedHeight, slide_info) {
            var animations = [];
            var animatedSlides = [];
            var slide_left = 100 + this.opts.slideMarginPercent;

            slider.beforeSlide($toSlide);

            // определяем слайды, учавствующие в анимации
            if (this.opts.showIntermediate) {
                var i = 0;
                var $slide = slider.$currentSlide;
                while ($slide.length && (i++ <= slide_info.count)) {
                    animatedSlides.push($slide);

                    $slide = slider.getPreviousSlide($slide);
                }
            } else {
                animatedSlides.push(slider.$currentSlide);
                animatedSlides.push($toSlide);
            }

            // заполнение данных о анимации каждого слайда
            var animatedSlidesCount = animatedSlides.length;
            for (i = 0; i < animatedSlidesCount; i++) {
                var $animatedSlide = animatedSlides[i];

                var left = -i * slide_left;
                $animatedSlide.css({
                    left: left + '%'
                });
                animations.push({
                    $animatedSlide: $animatedSlide,
                    from_left: left,
                    to_left: left + ((animatedSlidesCount - 1) * slide_left)
                });
            }

            slider.setCurrentSlide($toSlide);

            slider._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        this.autoInit('slide_' + i, animation_data.from_left, animation_data.to_left);
                    }
                },
                step: function(eProgress) {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        animation_data.$animatedSlide.css({
                            left: this.autoCalc('slide_' + i, eProgress) + '%'
                        })
                    }
                },
                complete: function() {
                    for (var i = 0; i < (animations.length - 1); i++) {
                        var animation_data = animations[i];
                        animation_data.$animatedSlide.css({
                            left: ''
                        })
                    }
                    slider.afterSlide($toSlide);
                }
            });

            slider.updateListHeight(animatedHeight);
        };
    });


    //========================================================
    //  Анимация, выбирающая направление, соответствующее
    //  кратчайшему пути.
    //========================================================
    window.SliderSideShortestAnimation = Class(SliderSideAnimation, function(cls, superclass) {
        // Настройки по умолчанию
        cls.prototype.getDefaultOpts = function() {
            var defaults = superclass.prototype.getDefaultOpts.call(this);
            return $.extend(true, defaults, {
                name: 'side-shortest'
            });
        };

        /*
            Выбор направления анимации
         */
        cls.prototype.chooseSlideDirection = function(slider, $toSlide, animatedHeight, slide_info) {
            var diff = slide_info.toIndex - slide_info.fromIndex;

            if (slider.opts.loop) {
                var slides_count = slider.$slides.length;
                var right_way = diff + (diff > 0 ? 0 : slides_count);
                var left_way = (diff > 0 ? slides_count : 0) - diff;

                if (left_way < right_way) {
                    slide_info.count = left_way;
                    this.slideLeft.call(this, slider, $toSlide, animatedHeight, slide_info);
                } else {
                    slide_info.count = right_way;
                    this.slideRight.call(this, slider, $toSlide, animatedHeight, slide_info);
                }
            } else {
                if (slide_info.toIndex > slide_info.fromIndex) {
                    slide_info.count = diff;
                    this.slideRight.call(this, slider, $toSlide, animatedHeight, slide_info);
                } else {
                    slide_info.count = -diff;
                    this.slideLeft.call(this, slider, $toSlide, animatedHeight, slide_info);
                }
            }
        };
    });

})(jQuery);
