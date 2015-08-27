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

                thresholdPercents: 15,

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

                onStartDrag: function() {
                    // Запоминаем слайд, с которого начали перетаскивание
                    that.$startSlide = slider.$currentSlide;
                },
                onDrag: function(evt) {
                    that.onDrag(slider, evt);
                },
                onStopDrag: function(evt) {
                    var dxPercents = that._dxToPercents(slider, evt);
                    var absDxPercents = Math.abs(dxPercents);

                    var $currSlide = slider.$currentSlide;
                    if (evt.dx > 0) {
                        var $prevSlide = slider.getPreviousSlide($currSlide);
                        if ($prevSlide.length && (absDxPercents > that.opts.thresholdPercents)) {
                            that.dragChooseLeft(slider, $prevSlide, $currSlide);
                        } else {
                            that.dragChooseRight(slider, $prevSlide, $currSlide);
                        }
                    } else {
                        var $nextSlide = slider.getNextSlide($currSlide);
                        if ($nextSlide.length && (absDxPercents > that.opts.thresholdPercents)) {
                            that.dragChooseRight(slider, $currSlide, $nextSlide);
                        } else {
                            that.dragChooseLeft(slider, $currSlide, $nextSlide);
                        }
                    }
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
            Перетаскивание слайдов мышью или тачпадом
         */
        DragPlugin.prototype.onDrag = function(slider, evt) {
            if (slider._animated) {
                // если идет анимация - игнорируем
                this.drager.startPoint = evt.point;
                return
            }

            var dxPercents = this._dxToPercents(slider, evt);
            var absDxPercents = Math.abs(dxPercents);
            var slide_left = 100 + this.opts.slideMarginPercent;

            // метод перехода к соседнему слайду по направлению движения
            if (evt.dx > 0) {
                var getSideSlide = $.proxy(slider.getPreviousSlide, slider);
            } else {
                getSideSlide = $.proxy(slider.getNextSlide, slider);
            }

            var $floorSlide = this.$startSlide;


            // жесткий переход к слайду
            /*if (absDxPercents > slide_left) {
                slider.$slides.css({
                    left: ''
                });

                var passCount = Math.floor(absDxPercents);
                absDxPercents = absDxPercents - slide_left * passCount;
                this.drager.startPoint = evt.point;

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
                    left: absDxPercents + '%'
                });

                if ($sideSlide.length) {
                    $sideSlide.css({
                        left: absDxPercents - slide_left + '%'
                    });
                }
            } else {
                // тащим влево
                $currSlide.css({
                    left: -absDxPercents + '%'
                });

                if ($sideSlide.length) {
                    $sideSlide.css({
                        left: -absDxPercents + slide_left + '%'
                    });
                }
            }*/
        };

        DragPlugin.prototype.dragChooseLeft = function(slider, $leftSlide, $rightSlide) {
            var slide_left = 100 + this.opts.slideMarginPercent;
            var offsetPercentage = -parseFloat($leftSlide.get(0).style.left);
            var duration = Math.round(this.opts.speed * offsetPercentage / 100);
            duration = Math.max(100, duration);

            slider.beforeSlide($leftSlide);
            slider._setCurrentSlide($leftSlide);
            slider._animation = $.animate({
                duration: duration,
                delay: 40,
                easing: this.opts.easing,
                init: function() {
                    this.left_initial = parseFloat($leftSlide.get(0).style.left);
                    this.left_diff = -this.left_initial;
                    if ($rightSlide.length) {
                        this.right_initial = parseFloat($rightSlide.get(0).style.left);
                        this.right_diff = slide_left - this.right_initial;
                    }
                },
                step: function(eProgress) {
                    $leftSlide.css({
                        left: this.left_initial + this.left_diff * eProgress + '%'
                    });
                    $rightSlide.css({
                        left: this.right_initial + this.right_diff * eProgress + '%'
                    });
                },
                complete: function() {
                    $rightSlide.css({
                        left: ''
                    });
                    slider.afterSlide($leftSlide);
                }
            });

            slider.updateListHeight(this.opts.animatedHeight);
        };

        DragPlugin.prototype.dragChooseRight = function(slider, $leftSlide, $rightSlide) {
            var slide_left = 100 + this.opts.slideMarginPercent;
            var offsetPercentage = parseFloat($rightSlide.get(0).style.left);
            var duration = Math.round(this.opts.speed * offsetPercentage / 100);
            duration = Math.max(100, duration);

            slider.beforeSlide($rightSlide);
            slider._setCurrentSlide($rightSlide);
            slider._animation = $.animate({
                duration: duration,
                delay: 40,
                easing: this.opts.easing,
                init: function() {
                    if ($leftSlide.length) {
                        this.left_initial = parseFloat($leftSlide.get(0).style.left);
                        this.left_diff = -slide_left - this.left_initial;
                    }
                    this.right_initial = parseFloat($rightSlide.get(0).style.left);
                    this.right_diff = -this.right_initial;
                },
                step: function(eProgress) {
                    $leftSlide.css({
                        left: this.left_initial + this.left_diff * eProgress + '%'
                    });
                    $rightSlide.css({
                        left: this.right_initial + this.right_diff * eProgress + '%'
                    });
                },
                complete: function() {
                    $leftSlide.css({
                        left: ''
                    });
                    slider.afterSlide($rightSlide);
                }
            });

            slider.updateListHeight(this.opts.animatedHeight);
        };

        return DragPlugin;
    })(SliderPlugin);

})(jQuery);
