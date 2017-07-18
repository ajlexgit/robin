(function($) {
    'use strict';

    window.SliderDragPlugin = Class(SliderPlugin, function SliderDragPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animateListHeight: true,

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

        /*
            Включение плагина
         */
        cls.enable = function() {
            this.drager.attach();
            superclass.enable.call(this);
        };

        /*
            Выключение плагина
         */
        cls.disable = function() {
            this.drager.detach();
            superclass.disable.call(this);
        };

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
            this.getContainer();
            this.drager = Drager(this.$container, {
                mouse: this.opts.mouse,
                touch: this.opts.touch,
                ignoreDistanceX: this.opts.ignoreDistanceX,
                ignoreDistanceY: this.opts.ignoreDistanceY,
                momentum: false
            }).on('dragstart', function(evt) {
                // если один слайд - выходим
                if (that.slider.$slides.length < 2) {
                    this.setStartPoint(evt);
                    return false;
                }

                // если идет анимация - прекращаем её
                that.slider.stopAnimation(true);

                // добавляем overflow, чтобы не было видно соседних слайдов
                that.slider.$list.css({
                    overflow: 'hidden'
                });

                that.onStartDrag(evt);
            }).on('drag', function(evt) {
                if (evt.dx === that._dx) {
                    return false;
                }

                if (evt.abs_dx > evt.abs_dy) {
                    // по X движение больше
                    that.onDrag(evt);
                    return false
                }
            }).on('dragend', function(evt) {
                that.onStopDrag(evt);
            });

            this._updateEnabledState();
            this.checkUnselectable();
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        cls.afterSetItemsPerSlide = function() {
            this._updateEnabledState();
            this.checkUnselectable();
        };

        /*
            Блокировка плагина
         */
        cls.onResize = function() {
            this._updateEnabledState();
            superclass.onResize.call(this);
        };

        /*
            Проверка, нужно ли блокировать выделение текста
         */
        cls.checkUnselectable = function() {
            if (this.slider.$slides.length >= 2) {
                this.slider.$root.addClass('unselectable');
            } else {
                this.slider.$root.removeClass('unselectable');
            }
        };

        /*
            Перевод смещения в пикселях в смещение в процентах
         */
        cls._dxToPercents = function(evt) {
            return 100 * evt.dx / this.slider.$list.outerWidth();
        };

        /*
            Перевод отступа в пикселях в отступ в процентах
         */
        cls._getPercentGap = function() {
            if (this.opts.margin.toString().indexOf('%') >= 0) {
                return parseFloat(this.opts.margin);
            } else {
                return 100 * parseFloat(this.opts.margin) / this.slider.$list.outerWidth();
            }
        };

        /*
            Получение контейнера для элементов
         */
        cls.getContainer = function() {
            if (typeof this.opts.container === 'string') {
                this.$container = this.slider.$root.find(this.opts.container);
            } else if ($.isFunction(this.opts.container)) {
                this.$container = this.opts.container.call(this);
            } else if (this.opts.container && this.opts.container.jquery) {
                this.$container = this.opts.container;
            }

            if (!this.$container || !this.$container.length) {
                this.$container = this.slider.$listWrapper;
            } else if (this.$container.length) {
                this.$container = this.$container.first();
            }
        };

        /*
            Начало перетаскивания слайдов мышью или тачпадом
         */
        cls.onStartDrag = function() {
            // Запоминаем слайд, с которого начали перетаскивание
            this.$startSlide = this.slider.$currentSlide;

            this._dx = 0;
            this._movedSlides = [];

            this.slider.trigger('startDrag');
            this.slider.callPluginsMethod('startDrag');
        };

        /*
            Перетаскивание слайдов мышью или тачпадом
         */
        cls.onDrag = function(evt) {
            var dxPercents = this._dxToPercents(evt);
            var absDxPercents = Math.abs(dxPercents);
            var slide_left = 100 + this._getPercentGap();

            // метод перехода к соседнему слайду по направлению движения
            if (evt.dx > 0) {
                this._getSideSlide = $.proxy(
                    this.slider.getPreviousSlide,
                    this.slider
                );
            } else {
                this._getSideSlide = $.proxy(
                    this.slider.getNextSlide,
                    this.slider
                );
            }

            // очищаем позицию слайдов, которые перемещались ранее
            $(this._movedSlides.filter(Boolean)).css({
                transform: ''
            });

            // находим видимый слайд, ближайший к точке начала движения
            var passSlideCount = Math.floor(absDxPercents / slide_left);
            if (passSlideCount > 0) {
                var $nearSlide = this._getSideSlide(this.$startSlide, passSlideCount - 1);
                if (!$nearSlide.length || (this.slider.$slides.length < 2)) {
                    return
                }
            } else {
                $nearSlide = this.$startSlide;
            }

            // нормализация процента смещения
            absDxPercents = absDxPercents % slide_left;

            // определяем активный слайд
            var slider_width = this.slider.$list.outerWidth();
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
            if (this.slider.$currentSlide.get(0) !== $newCurrentSlide.get(0)) {
                this.slider._setCurrentSlide($newCurrentSlide);
                this.slider.softUpdateListHeight(this.opts.animateListHeight);
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
        cls.onStopDrag = function(evt) {
            if (!this._movedSlides || (this._movedSlides.length !== 2)) {
                return
            }

            var leftSlide = this._movedSlides[0];
            var rightSlide = this._movedSlides[1];
            var $currSlide = this.slider.$currentSlide;

            var slide_left = 100 + this._getPercentGap();

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


            var that = this;
            var $leftSlide = $(leftSlide);
            var $rightSlide = $(rightSlide);
            this.slider._beforeSlide($currSlide);
            this.slider._animation = $(animation_from).animate(animation_to, {
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

                    that.slider.$list.css({
                        overflow: ''
                    });

                    that.slider._afterSlide($currSlide);
                }
            });

            this.slider.callPluginsMethod('stopDrag', null, true);
            this.slider.trigger('stopDrag');
        };
    });

})(jQuery);
