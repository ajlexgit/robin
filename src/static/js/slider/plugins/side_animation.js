(function($) {
    'use strict';

    window.SliderSideAnimation = Class(SliderPlugin, function SliderSideAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'side',

            margin: 0,          // в пикселях или процентах
            speed: 800,
            showIntermediate: true,
            easing: 'easeOutCubic'
        });

        /*
            Перевод отступа в пикселях в отступ в процентах
         */
        cls._getPercentGap = function(slider) {
            if (this.opts.margin.toString().indexOf('%') >= 0) {
                return parseFloat(this.opts.margin);
            } else {
                var slider_width = slider.$list.outerWidth();
                return 100 * parseFloat(this.opts.margin) / slider_width;
            }
        };

        /*
            Реализация метода перехода от одного слайда к другому
            посредством выдвигания с края слайдера
         */
        cls.slideTo = function(slider, $toSlide, animatedHeight) {
            if (slider._animation) {
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
        cls.chooseSlideDirection = function(slider, $toSlide, animatedHeight, slide_info) {
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
            Создание анимации перехода
         */
        cls._slide = function(slider, $toSlide, animations) {
            var animation_from = {};
            var animation_to = {};
            animations.forEach(function(animation_data, index) {
                var name = 'slide_' + index;
                animation_from[name] = animation_data.from_left;
                animation_to[name] = animation_data.to_left;
            });

            slider._animation = $(animation_from).animate(animation_to, {
                duration: this.opts.speed,
                easing: this.opts.easing,
                progress: function() {
                    var conf = this;
                    animations.forEach(function(animation_data, index) {
                        animation_data.$animatedSlide.css({
                            left: conf['slide_' + index] + '%'
                        })
                    });
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
        };

        /*
            Появление нового слайда справа от текущего
         */
        cls.slideRight = function(slider, $toSlide, animatedHeight, slide_info) {
            var animations = [];
            var animatedSlides = [];
            var slide_left = 100 + this._getPercentGap(slider);

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
            animatedSlides.forEach(function($animatedSlide, index) {
                var left = index * slide_left;
                $animatedSlide.css({
                    left: left + '%'
                });
                animations.push({
                    $animatedSlide: $animatedSlide,
                    from_left: left,
                    to_left: left - ((animatedSlidesCount - 1) * slide_left)
                });
            });

            slider._setCurrentSlide($toSlide);
            this._slide(slider, $toSlide, animations);
            slider.updateListHeight(animatedHeight);
        };

        /*
            Появление нового слайда слева от текущего
         */
        cls.slideLeft = function(slider, $toSlide, animatedHeight, slide_info) {
            var animations = [];
            var animatedSlides = [];
            var slide_left = 100 + this._getPercentGap(slider);

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
            animatedSlides.forEach(function($animatedSlide, index) {
                var left = -index * slide_left;
                $animatedSlide.css({
                    left: left + '%'
                });
                animations.push({
                    $animatedSlide: $animatedSlide,
                    from_left: left,
                    to_left: left + ((animatedSlidesCount - 1) * slide_left)
                });
            });

            slider._setCurrentSlide($toSlide);
            this._slide(slider, $toSlide, animations);
            slider.updateListHeight(animatedHeight);
        };
    });


    //========================================================
    //  Анимация, выбирающая направление, соответствующее
    //  кратчайшему пути.
    //========================================================
    window.SliderSideShortestAnimation = Class(SliderSideAnimation, function SliderSideShortestAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'side-shortest'
        });


        /*
            Выбор направления анимации
         */
        cls.chooseSlideDirection = function(slider, $toSlide, animatedHeight, slide_info) {
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
