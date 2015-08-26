(function($) {

    window.SliderSideAnimation = (function(parent) {
        // Инициализация плагина
        var SideAnimation = function(settings) {
            parent.call(this, settings);
        };

        var _ = function() {
            this.constructor = SideAnimation;
        };
        _.prototype = parent.prototype;
        SideAnimation.prototype = new _;


        // Настройки по умолчанию
        SideAnimation.prototype.getDefaultOpts = function() {
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
        SideAnimation.prototype.slideTo = function(slider, $toSlide, animatedHeight) {
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
        SideAnimation.prototype.chooseSlideDirection = function(slider, $toSlide, animatedHeight, slide_info) {
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
        SideAnimation.prototype.slideRight = function(slider, $toSlide, animatedHeight, slide_info) {
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

            slider._setCurrentSlide($toSlide);

            this._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        animation_data.diff = animation_data.to_left - animation_data.from_left;
                    }
                },
                step: function(eProgress) {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        var left = animation_data.from_left + animation_data.diff * eProgress;
                        animation_data.$animatedSlide.css({
                            left: left + '%'
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
        SideAnimation.prototype.slideLeft = function(slider, $toSlide, animatedHeight, slide_info) {
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

            slider._setCurrentSlide($toSlide);

            this._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        animation_data.diff = animation_data.to_left - animation_data.from_left;
                    }
                },
                step: function(eProgress) {
                    for (var i = 0; i < animations.length; i++) {
                        var animation_data = animations[i];
                        var left = animation_data.from_left + animation_data.diff * eProgress;
                        animation_data.$animatedSlide.css({
                            left: left + '%'
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
            Начало перетаскивания слайда
         */
        SideAnimation.prototype.dragStart = function(slider, drag_plugin, evt) {

        };

        SideAnimation.prototype._dxToPercents = function(slider, dx) {
            var slider_width = slider.$list.outerWidth();
            return 100 * dx / slider_width
        };

        /*
            Перетаскивание слайдов мышью или тачпадом
         */
        SideAnimation.prototype.drag = function(slider, drag_plugin, evt) {
            if (slider._animated) {
                drag_plugin.drager.startPoint = evt.point;
                return
            }

            var $currSlide, $sideSlide;
            var dxPercents = this._dxToPercents(evt.dx);
            var absDxPercents = Math.abs(dxPercents);
            var slide_left = 100 + this.opts.slideMarginPercent;

            // метод перехода к соседнему слайду по направлению движения
            if (evt.dx > 0) {
                var getSideSlide = $.proxy(slider.getPreviousSlide, slider);
            } else {
                getSideSlide = $.proxy(slider.getNextSlide, slider);
            }

            // жесткий переход к слайду
            if (absDxPercents > slide_left) {
                slider.$slides.css({
                    left: ''
                });

                var passCount = Math.floor(dxPercents);
                absDxPercents = absDxPercents - slide_left * passCount;
                drag_plugin.drager.startPoint = evt.point;

                var i = 0;
                $currSlide = slider.$currentSlide;
                while (i++ < passCount) {
                    $sideSlide = getSideSlide($currSlide);
                    if ($sideSlide.length) {
                        $currSlide = $sideSlide;
                    } else {
                        break
                    }
                }

                slider.beforeSlide($currSlide);
                slider._setCurrentSlide($currSlide);
                slider.afterSlide($currSlide);

                slider.updateListHeight();
            }

            $currSlide = slider.$currentSlide;
            $sideSlide = getSideSlide($currSlide);
            if (evt.dx > 0) {
                // тащим вправо
                $currSlide.css({
                    left: absDxPercents
                });
                $sideSlide.css({
                    left: absDxPercents - slide_left
                });
            } else {
                // тащим влево
                $currSlide.css({
                    left: -absDxPercents
                });
                $sideSlide.css({
                    left: -absDxPercents + slide_left
                });
            }
        };


        /*
            Завершение перетаскивания слайда
         */
        SideAnimation.prototype.dragStop = function(slider, drag_plugin, evt) {
            var dxPercents = this._dxToPercents(evt.dx);
            var absDxPercents = Math.abs(dxPercents);

            var $currSlide = slider.$currentSlide;
            if (evt.dx > 0) {
                var $prevSlide = slider.getPreviousSlide($currSlide);
                if (absDxPercents > drag_plugin.opts.minSlidePercent) {
                    this.dragChooseLeft(slider, $prevSlide, $currSlide);
                } else {
                    this.dragChooseRight(slider, $prevSlide, $currSlide);
                }
            } else {
                var $nextSlide = slider.getNextSlide($currSlide);
                if (absDxPercents > drag_plugin.opts.minSlidePercent) {
                    this.dragChooseLeft(slider, $currSlide, $nextSlide);
                } else {
                    this.dragChooseRight(slider, $currSlide, $nextSlide);
                }
            }
        };

        SideAnimation.prototype.dragChooseLeft = function(slider, $leftSlide, $rightSlide) {
            slider.beforeSlide($leftSlide);
            slider._setCurrentSlide($leftSlide);
            slider._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {

                },
                step: function(eProgress) {

                },
                complete: function() {
                    $rightSlide.css({
                        left: ''
                    });
                    slider.afterSlide($leftSlide);
                }
            });
        };

        SideAnimation.prototype.dragChooseRight = function(slider, $leftSlide, $rightSlide) {
            slider.beforeSlide($rightSlide);
            slider._setCurrentSlide($rightSlide);
            slider._animation = $.animate({
                duration: this.opts.speed,
                easing: this.opts.easing,
                init: function() {

                },
                step: function(eProgress) {

                },
                complete: function() {
                    $leftSlide.css({
                        left: ''
                    });
                    slider.afterSlide($rightSlide);
                }
            });
        };

        return SideAnimation;
    })(SliderPlugin);


    //========================================================
    //  Анимация, выбирающая направление, соответствующее
    //  кратчайшему пути.
    //========================================================
    window.SliderSideShortestAnimation = (function(parent) {
        var SideShortestAnimation = function(settings) {
            parent.call(this, settings);
        };

        var _ = function() {
            this.constructor = SideShortestAnimation;
        };
        _.prototype = parent.prototype;
        SideShortestAnimation.prototype = new _;


        // Настройки по умолчанию
        SideShortestAnimation.prototype.getDefaultOpts = function() {
            var defaults = parent.prototype.getDefaultOpts.call(this);
            return $.extend(true, defaults, {
                name: 'side-shortest'
            });
        };

        /*
            Выбор направления анимации
         */
        SideShortestAnimation.prototype.chooseSlideDirection = function(slider, $toSlide, animatedHeight, slide_info) {
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

        return SideShortestAnimation;
    })(SliderSideAnimation);

})(jQuery);
