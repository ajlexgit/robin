(function($) {
    'use strict';

    window.SliderDragPlugin = Class(SliderPlugin, function SliderDragPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animatedHeight: true,

            mouse: true,
            touch: true,
            ignoreDistanceX: 18,        // px
            ignoreDistanceY: 18,        // px

            slideThreshold: 10,         // %
            maxSlideThreshold: 50,      // px

            margin: 0,                  // в пикселях или процентах
            speed: 800,
            container: null,
            easing: 'easeOutCubic'
        });

        cls.destroy = function() {
            if (this.drager) {
                this.drager.destroy();
                this.drager = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Создание объекта Drager
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);

            var that = this;
            this.getContainer(slider);
            this.drager = Drager(this.$container, {
                mouse: this.opts.mouse,
                touch: this.opts.touch,
                ignoreDistanceX: this.opts.ignoreDistanceX,
                ignoreDistanceY: this.opts.ignoreDistanceY,
                momentum: false
            }).on('dragstart', function(evt) {
                // если один слайд - выходим
                if (slider.$slides.length < 2) {
                    this.setStartPoint(evt);
                    return false;
                }

                // если идет анимация - прекращаем её
                if (slider._animation) {
                    slider._animation.stop(true, true);
                    slider._animation = null;
                }

                slider.$list.css({
                    overflow: 'hidden'
                });
                slider.$slides.stop(true, true);
                that.onStartDrag(slider, evt);
            }).on('drag', function(evt) {
                if (evt.dx === that._dx) {
                    return false;
                }

                if (evt.abs_dx > evt.abs_dy) {
                    // по X движение больше
                    that.onDrag(slider, evt);
                    return false
                }
            }).on('dragend', function(evt) {
                that.onStopDrag(slider, evt);
            });

            this.checkEnabled(slider);
            this.checkUnselectable(slider);
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        cls.afterSetItemsPerSlide = function(slider) {
            this.checkEnabled(slider);
            this.checkUnselectable(slider);
        };

        /*
            Блокировка плагина
         */
        cls.onResize = function(slider) {
            this.checkEnabled(slider);
            superclass.onResize.call(this, slider);
        };

        /*
            Включение плагина
         */
        cls.enable = function(slider) {
            this.drager.attach();
            superclass.enable.call(this, slider);
        };

        /*
            Выключение плагина
         */
        cls.disable = function(slider) {
            this.drager.detach();
            superclass.disable.call(this, slider);
        };

        /*
            Проверка, нужно ли блокировать выделение текста
         */
        cls.checkUnselectable = function(slider) {
            if (slider.$slides.length >= 2) {
                slider.$root.addClass('unselectable');
            } else {
                slider.$root.removeClass('unselectable');
            }
        };

        /*
            Перевод смещения в пикселях в смещение в процентах
         */
        cls._dxToPercents = function(slider, evt) {
            var slider_width = slider.$list.outerWidth();
            return 100 * evt.dx / slider_width
        };

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
            Получение контейнера для элементов
         */
        cls.getContainer = function(slider) {
            if (typeof this.opts.container === 'string') {
                this.$container = slider.$root.find(this.opts.container);
            } else if ($.isFunction(this.opts.container)) {
                this.$container = this.opts.container.call(this, slider);
            } else if (this.opts.container && this.opts.container.jquery) {
                this.$container = this.opts.container;
            }

            if (!this.$container || !this.$container.length) {
                this.$container = slider.$listWrapper;
            } else if (this.$container.length) {
                this.$container = this.$container.first();
            }
        };

        /*
            Начало перетаскивания слайдов мышью или тачпадом
         */
        cls.onStartDrag = function(slider) {
            // Запоминаем слайд, с которого начали перетаскивание
            this.$startSlide = slider.$currentSlide;

            this._dx = 0;
            this._movedSlides = [];

            slider.trigger('start_drag');
            slider.callPluginsMethod('startDrag');
        };

        /*
            Перетаскивание слайдов мышью или тачпадом
         */
        cls.onDrag = function(slider, evt) {
            var dxPercents = this._dxToPercents(slider, evt);
            var absDxPercents = Math.abs(dxPercents);
            var slide_left = 100 + this._getPercentGap(slider);

            // метод перехода к соседнему слайду по направлению движения
            if (evt.dx > 0) {
                this._getSideSlide = $.proxy(slider.getPreviousSlide, slider);
            } else {
                this._getSideSlide = $.proxy(slider.getNextSlide, slider);
            }

            // очищаем позицию слайдов, которые перемещались ранее
            $(this._movedSlides.filter(Boolean)).css({
                transform: ''
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
            var farDirection = (evt.dx > 0) === (evt.dx >= this._dx);
            var threshold = Math.min(this.opts.maxSlideThreshold, slider_width * this.opts.slideThreshold / 100);
            if (farDirection) {
                var chooseFar = (absPixels > threshold);
            } else {
                chooseFar = ((slide_width - absPixels) < threshold);
            }


            // перемещаем ближний слайд
            var nearSlidePosition = evt.dx > 0 ? absDxPercents : -absDxPercents;
            $nearSlide.css({
                transform: 'translate(' + nearSlidePosition + '%, 0%)'
            });

            // Находим второй видимый слайд
            var $farSlide = this._getSideSlide($nearSlide);
            if ($farSlide.get(0) === $nearSlide.get(0)) {
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
                    transform: 'translate(' + farSlidePosition + '%, 0%)'
                });
            }


            // выделяем активный слайд
            if (slider.$currentSlide.get(0) !== $newCurrentSlide.get(0)) {
                slider._setCurrentSlide($newCurrentSlide);
                slider.softUpdateListHeight(this.opts.animatedHeight);
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
            if (!this._movedSlides || (this._movedSlides.length !== 2)) {
                return
            }

            var leftSlide = this._movedSlides[0];
            var rightSlide = this._movedSlides[1];
            var $currSlide = slider.$currentSlide;

            var slide_left = 100 + this._getPercentGap(slider);

            // определение анимации
            var transformRegex = /translate\(([-\d.]+)%,/i;
            var left_match = leftSlide && transformRegex.exec(leftSlide.style.transform);
            left_match = (left_match && parseFloat(left_match[1])) || 0;
            var right_match = rightSlide && transformRegex.exec(rightSlide.style.transform);
            right_match = (right_match && parseFloat(right_match[1])) || 0;

            var animation_from = {
                left_slide: left_match,
                right_slide: right_match
            };
            if ($currSlide.get(0) === leftSlide) {
                var animation_to = {
                    left_slide: 0,
                    right_slide: slide_left
                };
                var duration = Math.round(this.opts.speed * Math.abs(animation_from.left_slide) / 100);
            } else {
                animation_to = {
                    left_slide: -slide_left,
                    right_slide: 0
                };
                duration = Math.round(this.opts.speed * Math.abs(animation_from.right_slide) / 100);
            }


            var $leftSlide = $(leftSlide);
            var $rightSlide = $(rightSlide);
            slider.beforeSlide($currSlide);
            slider._animation = $(animation_from).animate(animation_to, {
                duration: Math.max(200, duration),
                easing: this.opts.easing,
                progress: function() {
                    $leftSlide.css({
                        transform: 'translate(' + this.left_slide + '%, 0%)'
                    });
                    $rightSlide.css({
                        transform: 'translate(' + this.right_slide + '%, 0%)'
                    });
                },
                complete: function() {
                    if ($currSlide.get(0) === leftSlide) {
                        $leftSlide.css({
                            transform: 'none'
                        });
                        $rightSlide.css({
                            transform: ''
                        });
                    } else {
                        $leftSlide.css({
                            transform: ''
                        });
                        $rightSlide.css({
                            transform: 'none'
                        });
                    }

                    slider.$list.css({
                        overflow: ''
                    });
                    slider.afterSlide($currSlide);
                }
            });

            slider.callPluginsMethod('stopDrag', null, true);
            slider.trigger('stop_drag');
        };
    });

})(jQuery);
