(function($) {
    'use strict';

    var DIRECTION_RIGHT = 'right';
    var DIRECTION_LEFT = 'left';

    window.SliderSideAnimation = Class(SliderPlugin, function SliderSideAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'side',

            margin: 0,          // в пикселях или процентах
            speed: 600,
            stoppable: true,
            easing: 'easeOutCubic',
            showIntermediate: true
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
                if (this.opts.stoppable) {
                    slider._animation.stop(true, true);
                    slider._animation = null;
                } else {
                    return
                }
            }

            var slide_info = {
                fromIndex: slider.$slides.index(slider.$currentSlide),
                toIndex: slider.$slides.index($toSlide)
            };

            // тот же слайд?
            if (slide_info.fromIndex == slide_info.toIndex) {
                return
            }

            // выбор направления анимации
            this.chooseSlideDirection(slider, slide_info);

            slider.beforeSlide($toSlide);
            var animations = this._make_animations(slider, $toSlide, slide_info);

            slider._setCurrentSlide($toSlide);
            this._animate(slider, $toSlide, animations);
            slider.softUpdateListHeight(animatedHeight);
        };

        /*
            Выбор направления анимации
         */
        cls.chooseSlideDirection = function(slider, slide_info) {
            var diff = slide_info.toIndex - slide_info.fromIndex;

            if (slide_info.toIndex > slide_info.fromIndex) {
                slide_info.count = diff;
                slide_info.direction = DIRECTION_RIGHT;
            } else {
                slide_info.count = -diff;
                slide_info.direction = DIRECTION_LEFT;
            }
        };

        /*
            Создание объектов для анимирования
         */
        cls._make_animations = function(slider, $toSlide, slide_info) {
            var animations = [];
            var animatedSlides = [];
            var slide_left = 100 + this._getPercentGap(slider);

            if (slide_info.direction == DIRECTION_RIGHT) {
                var doStepSlide = slider.getNextSlide.bind(slider);
            } else {
                doStepSlide = slider.getPreviousSlide.bind(slider);
            }

            // определяем слайды, учавствующие в анимации
            if (this.opts.showIntermediate) {
                var i = 0;
                var $slide = slider.$currentSlide;
                while ($slide.length && (i++ <= slide_info.count)) {
                    animatedSlides.push($slide);
                    $slide = doStepSlide($slide);
                }
            } else {
                animatedSlides.push(slider.$currentSlide);
                animatedSlides.push($toSlide);
            }

            // заполнение данных о анимации каждого слайда
            var animatedSlidesCount = animatedSlides.length;
            var direction_multiplier = slide_info.direction == DIRECTION_RIGHT ? 1 : -1;
            animatedSlides.forEach(function($animatedSlide, index) {
                var left = index * slide_left * direction_multiplier;
                $animatedSlide.css({
                    transform: 'translate(' + left +'%, 0%)'
                });
                animations.push({
                    $animatedSlide: $animatedSlide,
                    from_left: left,
                    to_left: left - ((animatedSlidesCount - 1) * slide_left * direction_multiplier)
                });
            });

            return animations;
        };

        /*
            Создание анимации перехода
         */
        cls._animate = function(slider, $toSlide, animations) {
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
                            transform: 'translate(' + conf['slide_' + index] + '%, 0%)'
                        })
                    });
                },
                complete: function() {
                    for (var i = 0; i < (animations.length - 1); i++) {
                        var animation_data = animations[i];
                        animation_data.$animatedSlide.css({
                            transform: ''
                        })
                    }
                    slider.afterSlide($toSlide);
                }
            });
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
        cls.chooseSlideDirection = function(slider, slide_info) {
            var diff = slide_info.toIndex - slide_info.fromIndex;

            if (slider.opts.loop) {
                var slides_count = slider.$slides.length;
                var right_way = diff + (diff > 0 ? 0 : slides_count);
                var left_way = (diff > 0 ? slides_count : 0) - diff;

                if (left_way < right_way) {
                    slide_info.count = left_way;
                    slide_info.direction = DIRECTION_LEFT;
                } else {
                    slide_info.count = right_way;
                    slide_info.direction = DIRECTION_RIGHT;
                }
            } else {
                if (slide_info.toIndex > slide_info.fromIndex) {
                    slide_info.count = diff;
                    slide_info.direction = DIRECTION_RIGHT;
                } else {
                    slide_info.count = -diff;
                    slide_info.direction = DIRECTION_LEFT;
                }
            }
        };
    });

})(jQuery);
