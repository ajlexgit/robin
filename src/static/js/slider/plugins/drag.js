(function($) {

    window.SliderDragPlugin = (function(parent) {
        // Инициализация плагина
        var DragPlugin = function(settings) {
            parent.call(this, settings);
        };

        var _ = function() {
            this.constructor = DragPlugin;
        };
        _.prototype = parent.prototype;
        DragPlugin.prototype = new _;


        // Настройки по умолчанию
        DragPlugin.prototype.getDefaultOpts = function() {
            return {
                mouse: true,
                touch: true,
                ignoreDistance: 10,

                slideThreshold: 50,

                speed: 800,
                easing: 'easeOutCubic',
                animatedHeight: true,
                slideMarginPercent: 0
            };
        };

        /*
            Создание объекта Drager
         */
        DragPlugin.prototype.onAttach = function(slider) {
            parent.prototype.onAttach.call(this, slider);

            var that = this;
            this.drager = new Drager(slider.$listWrapper, {
                mouse: this.opts.mouse,
                touch: this.opts.touch,
                ignoreDistance: this.opts.ignoreDistance,
                momentum: false,

                onStartDrag: function(evt) {
                    that.onStartDrag(slider, evt);
                },
                onDrag: function(evt) {
                    if (slider._animated) {
                        // если идет анимация - игнорируем
                        this.startPoint = evt.point;
                        return
                    }

                    that.onDrag(slider, evt);
                },
                onStopDrag: function(evt) {
                    that.onStopDrag(slider, evt);
                }
            })
        };

        /*
            Перевод смещения в пикселях в смещение в процентах
         */
        DragPlugin.prototype._dxToPercents = function(slider, evt) {
            var slider_width = slider.$list.outerWidth();
            return 100 * evt.dx / slider_width
        };


        /*
            Начало перетаскивания слайдов мышью или тачпадом
         */
        DragPlugin.prototype.onStartDrag = function(slider, evt) {
            // Запоминаем слайд, с которого начали перетаскивание
            this.$startSlide = slider.$currentSlide;

            this._oldDx = 0;
            this._oldMovedSlides = $();
        };


        /*
            Перетаскивание слайдов мышью или тачпадом
         */
        DragPlugin.prototype.onDrag = function(slider, evt) {
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
            this._oldMovedSlides.css({
                left: ''
            });

            // находим пару слайдов, которые видимы в данный момент
            var passSlideCount = Math.floor(absDxPercents / slide_left);
            if (passSlideCount > 0) {
                var $nearSlide = this._getSideSlide(this.$startSlide, passSlideCount - 1);
                if (!$nearSlide.length || (slider.$slides.length < 2)) {
                    return
                }
            } else {
                $nearSlide = this.$startSlide;
            }

            var $farSlide = this._getSideSlide($nearSlide);
            if ($farSlide.get(0) == $nearSlide.get(0)) {
                $farSlide = $();
            }

            // нормализация процента смещения
            absDxPercents = absDxPercents % slide_left;

            // определяем активный слайд
            var listWidth = slider.$list.outerWidth();
            var absPixels = Math.abs(evt.dx) % listWidth;
            var farDirection = (evt.dx > 0) == (evt.dx > this._oldDx);
            if (farDirection) {
                var chooseFar = (absPixels > this.opts.slideThreshold);
            } else {
                chooseFar = ((listWidth - absPixels) < this.opts.slideThreshold);
            }

            var $newCurrentSlide;
            if (chooseFar && $farSlide.length) {
                $newCurrentSlide = $farSlide;
            } else {
                $newCurrentSlide = $nearSlide;
            }

            // выделяем активный слайд
            if (slider.$currentSlide.get(0) != $newCurrentSlide.get(0)) {
                slider.beforeSlide($newCurrentSlide);
                slider.setCurrentSlide($newCurrentSlide);
                slider.afterSlide($newCurrentSlide);
                slider.updateListHeight(this.opts.animatedHeight);
            }

            // перемещение текущих слайдов
            var nearSlidePosition = evt.dx > 0 ? absDxPercents : -absDxPercents;
            $nearSlide.css({
                left: nearSlidePosition + '%'
            });

            if ($farSlide.length) {
                var farSlidePosition = evt.dx > 0 ? absDxPercents - slide_left : -absDxPercents + slide_left;
                $farSlide.css({
                    left: farSlidePosition + '%'
                });
            }

            this._oldDx = evt.dx;
            this._oldMovedSlides = $nearSlide.add($farSlide);
        };

        /*
            Завершение перетаскивания слайдов мышью или тачпадом
         */
        DragPlugin.prototype.onStopDrag = function(slider, evt) {
            var $currSlide = slider.$currentSlide;

            var $nextSlide = slider.getNextSlide($currSlide);
            if ($nextSlide.get(0) == $currSlide.get(0)) {
                $nextSlide = $()
            }

            var $prevSlide = slider.getPreviousSlide($currSlide);
            if ($prevSlide.get(0) == $currSlide.get(0)) {
                $prevSlide = $()
            }

            var slide_left = 100 + this.opts.slideMarginPercent;
            var currSlidePosition = parseFloat($currSlide.get(0).style.left);
            if (isNaN(currSlidePosition)) {
                currSlidePosition = evt.dx > 0 ? slide_left : -slide_left;
            }
            var duration = Math.round(this.opts.speed * Math.abs(currSlidePosition) / 100);

            slider.beforeSlide($currSlide);
            slider._animation = $.animate({
                duration: Math.max(200, duration),
                delay: 40,
                easing: this.opts.easing,
                init: function() {
                    this.curr_pos = currSlidePosition;
                    this.curr_diff = -currSlidePosition;

                    if ($nextSlide.length) {
                        this.next_pos = parseFloat($nextSlide.get(0).style.left);
                        this.next_diff = slide_left - this.next_pos;
                    }

                    if ($prevSlide.length) {
                        this.prev_pos = parseFloat($prevSlide.get(0).style.left);
                        this.prev_diff = -slide_left - this.prev_pos;
                    }
                },
                step: function(eProgress) {
                    $currSlide.css({
                        left: this.curr_pos + this.curr_diff * eProgress + '%'
                    });

                    $nextSlide.css({
                        left: this.next_pos + this.next_diff * eProgress + '%'
                    });

                    $prevSlide.css({
                        left: this.prev_pos + this.prev_diff * eProgress + '%'
                    });
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
        };

        return DragPlugin;
    })(SliderPlugin);

})(jQuery);
