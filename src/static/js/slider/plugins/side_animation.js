(function($) {
    'use strict';

    var DIRECTION_RIGHT = 'right';
    var DIRECTION_LEFT = 'left';

    window.SliderSideAnimation = Class(SliderPlugin, function SliderSideAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'side',

            margin: 0,          // в пикселях или процентах
            speed: 600,
            easing: 'easeOutCubic',
            showIntermediate: true
        });

        /*
            Перевод отступа в пикселях в отступ в процентах
         */
        cls._getPercentGap = function() {
            if (this.opts.margin.toString().indexOf('%') >= 0) {
                return parseFloat(this.opts.margin);
            } else {
                var slider_width = this.slider.$list.outerWidth();
                return 100 * parseFloat(this.opts.margin) / slider_width;
            }
        };

        /*
            Реализация метода перехода от одного слайда к другому
            посредством выдвигания с края слайдера
         */
        cls.slideTo = function($toSlide, animateListHeight) {
            this.slider.stopAnimation(true);

            var slide_info = {
                fromIndex: this.slider.$slides.index(this.slider.$currentSlide),
                toIndex: this.slider.$slides.index($toSlide)
            };

            this.slider._beforeSlide($toSlide);

            // выбор направления анимации
            this.chooseSlideDirection(slide_info);
            var animations = this._make_animations($toSlide, slide_info);

            this.slider._setCurrentSlide($toSlide);
            this._animate($toSlide, animations);
            this.slider.softUpdateListHeight(animateListHeight);
        };

        /*
            Выбор направления анимации
         */
        cls.chooseSlideDirection = function(slide_info) {
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
        cls._make_animations = function($toSlide, slide_info) {
            var animations = [];
            var animatedSlides = [];
            var slide_left = 100 + this._getPercentGap();

            if (slide_info.direction === DIRECTION_RIGHT) {
                var doStepSlide = this.slider.getNextSlide.bind(this.slider);
            } else {
                doStepSlide = this.slider.getPreviousSlide.bind(this.slider);
            }

            // определяем слайды, учавствующие в анимации
            if (this.opts.showIntermediate) {
                var i = 0;
                var $slide = this.slider.$currentSlide;
                while ($slide.length && (i++ <= slide_info.count)) {
                    animatedSlides.push($slide);
                    $slide = doStepSlide($slide);
                }
            } else {
                animatedSlides.push(this.slider.$currentSlide);
                animatedSlides.push($toSlide);
            }

            // заполнение данных о анимации каждого слайда
            var animatedSlidesCount = animatedSlides.length;
            var direction_multiplier = slide_info.direction === DIRECTION_RIGHT ? 1 : -1;
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
        cls._animate = function($toSlide, animations) {
            var animation_from = {};
            var animation_to = {};
            animations.forEach(function(animation_data, index) {
                var name = 'slide_' + index;
                animation_from[name] = animation_data.from_left;
                animation_to[name] = animation_data.to_left;
            });

            this.slider.$list.css({
                overflow: 'hidden'
            });

            var that = this;
            this.slider._animation = $(animation_from).animate(animation_to, {
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

                    that.slider.$list.css({
                        overflow: ''
                    });

                    that.slider._afterSlide($toSlide);
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
        cls.chooseSlideDirection = function(slide_info) {
            var diff = slide_info.toIndex - slide_info.fromIndex;
            if (this.slider.opts.loop) {
                var slides_count = this.slider.$slides.length;
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
