(function($) {

    window.SliderDragPlugin = Class(SliderPlugin, function SliderDragPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            mouse: true,
            touch: true,
            ignoreDistanceX: 18,        // px
            ignoreDistanceY: 18,        // px

            slideThreshold: 10,         // %
            maxSlideThreshold: 50,      // px

            speed: 800,
            dragOneSlide: false,
            easing: 'easeOutCubic',
            animatedHeight: true,
            slideMarginPercent: 0
        });

        /*
            Создание объекта Drager
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);

            var that = this;
            this.drager = Drager(slider.$listWrapper, {
                mouse: that.opts.mouse,
                touch: that.opts.touch,
                ignoreDistanceX: that.opts.ignoreDistanceX,
                ignoreDistanceY: that.opts.ignoreDistanceY,
                momentum: false,

                onStartDrag: function(evt) {
                    if (!that.opts.dragOneSlide && (slider.$slides.length < 2)) {
                        // если один слайд - выходим
                        this.setStartPoint(evt);
                        return false;
                    }

                    that.onStartDrag(slider, evt);

                    if (slider._animated) {
                        // если идет анимация - прекращаем её
                        if (slider._animation) {
                            slider._animation.stop(true);
                            slider._animation = null;
                        }
                    }
                },
                onDrag: function(evt) {
                    if (evt.dx == that._dx) {
                        return false;
                    }

                    if (evt.abs_dx > evt.abs_dy) {
                        // по X движение больше
                        that.onDrag(slider, evt);
                        return false
                    }
                },
                onStopDrag: function(evt) {
                    that.onStopDrag(slider, evt);
                }
            })
        };

        /*
            Перевод смещения в пикселях в смещение в процентах
         */
        cls._dxToPercents = function(slider, evt) {
            var slider_width = slider.$list.outerWidth();
            return 100 * evt.dx / slider_width
        };

        /*
            Начало перетаскивания слайдов мышью или тачпадом
         */
        cls.onStartDrag = function(slider) {
            // Запоминаем слайд, с которого начали перетаскивание
            this.$startSlide = slider.$currentSlide;

            this._dx = 0;
            this._movedSlides = [];

            // jQuery event
            slider.$list.trigger('startDrag.slider');

            slider.callPluginsMethod('startDrag');
        };

        /*
            Перетаскивание слайдов мышью или тачпадом
         */
        cls.onDrag = function(slider, evt) {
            var dxPercents = this._dxToPercents(slider, evt);
            var absDxPercents = Math.abs(dxPercents);
            var slide_left = 100 + this.opts.slideMarginPercent;

            // метод перехода к соседнему слайду по направлению движения
            if (evt.dx > 0) {
                this._getSideSlide = $.proxy(slider.getPreviousSlide, slider);
            } else {
                this._getSideSlide = $.proxy(slider.getNextSlide, slider);
            }

            // очищаем позицию слайдов, которые перемещались ранее
            $(this._movedSlides.filter(Boolean)).css({
                left: ''
            });

            // находим видимый слайд, ближайший к точке начала движения
            var passSlideCount = Math.floor(absDxPercents / slide_left);
            if (passSlideCount > 0) {
                var $nearSlide = this._getSideSlide(this.$startSlide, passSlideCount - 1);
                if (!$nearSlide.length || (slider.$slides.length < 2)) {
                    return
                }
            } else {
                $nearSlide = this.$startSlide;
            }

            // нормализация процента смещения
            absDxPercents = absDxPercents % slide_left;

            // определяем активный слайд
            var slider_width = slider.$list.outerWidth();
            var slide_width = slider_width * slide_left / 100;
            var absPixels = evt.abs_dx % slide_width;
            var farDirection = (evt.dx > 0) == (evt.dx >= this._dx);
            var threshold = Math.min(this.opts.maxSlideThreshold, slider_width * this.opts.slideThreshold / 100);
            if (farDirection) {
                var chooseFar = (absPixels > threshold);
            } else {
                chooseFar = ((slide_width - absPixels) < threshold);
            }


            // перемещаем ближний слайд
            var nearSlidePosition = evt.dx > 0 ? absDxPercents : -absDxPercents;
            $nearSlide.css({
                left: nearSlidePosition + '%'
            });

            // Находим второй видимый слайд
            var $farSlide = this._getSideSlide($nearSlide);
            if ($farSlide.get(0) == $nearSlide.get(0)) {
                $farSlide = $();
            }

            var $newCurrentSlide = $nearSlide;
            if ($farSlide.length) {
                if (chooseFar) {
                    $newCurrentSlide = $farSlide;
                }

                // перемещаем дальний слайд
                var farSlidePosition = evt.dx > 0 ? absDxPercents - slide_left : -absDxPercents + slide_left;
                $farSlide.css({
                    left: farSlidePosition + '%'
                });
            }


            // выделяем активный слайд
            if (slider.$currentSlide.get(0) != $newCurrentSlide.get(0)) {
                slider.beforeSlide($newCurrentSlide);
                slider.setCurrentSlide($newCurrentSlide);
                slider.afterSlide($newCurrentSlide);
                slider.updateListHeight(this.opts.animatedHeight);
            }


            this._dx = evt.dx;
            this._movedSlides = evt.dx > 0 ? [
                $farSlide.get(0), $nearSlide.get(0)
            ] : [
                $nearSlide.get(0), $farSlide.get(0)
            ];
        };

        /*
            Завершение перетаскивания слайдов мышью или тачпадом
         */
        cls.onStopDrag = function(slider, evt) {
            if (!this._movedSlides || (this._movedSlides.length != 2)) {
                return
            }

            var leftSlide = this._movedSlides[0];
            var rightSlide = this._movedSlides[1];
            var $currSlide = slider.$currentSlide;

            var slide_left = 100 + this.opts.slideMarginPercent;
            var currSlidePosition = parseFloat($currSlide.get(0).style.left);
            if (isNaN(currSlidePosition)) {
                currSlidePosition = evt.dx > 0 ? slide_left : -slide_left;
            }
            var duration = Math.round(this.opts.speed * Math.abs(currSlidePosition) / 100);

            slider.beforeSlide($currSlide);
            slider._animation = $.animate({
                duration: Math.max(200, duration),
                easing: this.opts.easing,
                init: function() {
                    this.autoInit('current_slide', currSlidePosition, 0);


                    if ($currSlide.get(0) == leftSlide) {
                        // второй слайд - правый
                        this.$otherSlide = $(rightSlide);
                        if (rightSlide) {
                            this.autoInit('other_slide', parseFloat(rightSlide.style.left), slide_left);
                        }
                    } else {
                        // второй слайд - левый
                        this.$otherSlide = $(leftSlide);
                        if (leftSlide) {
                            this.autoInit('other_slide', parseFloat(leftSlide.style.left), -slide_left);
                        }
                    }
                },
                step: function(eProgress) {
                    $currSlide.css({
                        left: this.autoCalc('current_slide', eProgress) + '%'
                    });

                    if (this.$otherSlide.length) {
                        this.$otherSlide.css({
                            left: this.autoCalc('other_slide', eProgress) + '%'
                        });
                    }
                },
                complete: function() {
                    slider.$slides.css({
                        left: ''
                    });

                    $currSlide.css({
                        left: '0'
                    });

                    slider.afterSlide($currSlide);
                }
            });

            slider.callPluginsMethod('stopDrag', null, true);

            // jQuery event
            slider.$list.trigger('stopDrag.slider');
        };
    });

})(jQuery);
