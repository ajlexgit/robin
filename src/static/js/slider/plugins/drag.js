(function($) {

    window.SliderDragPlugin = (function(parent) {
        // Инициализация плагина
        var DragPlugin = function(settings) {
            parent.call(this, settings);

            if (!this.opts.animationName) {
                console.error('Drag plugin must set animationName');
            }
        };

        var _ = function() {
            this.constructor = DragPlugin;
        };
        _.prototype = parent.prototype;
        DragPlugin.prototype = new _;


        // Настройки по умолчанию
        DragPlugin.prototype.getDefaultOpts = function() {
            return {
                animationName: '',
                animatedHeight: true,

                mouse: true,
                touch: true,
                ignoreDistance: 10
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
                    console.log('start', evt);
                },
                onDrag: function(evt) {
                    if (slider._animated) {
                        that.drager.startPoint = evt.point;
                        return
                    }

                    if (evt.dx > 0) {
                        // тащим вправо
                        that.dragRight(slider, evt);
                    } else {
                        // тащим влево
                        that.dragLeft(slider, evt);
                    }
                },
                onStopDrag: function(evt) {
                    console.log('stop', evt);
                }
            })
        };


        DragPlugin.prototype.dragLeft = function(slider, evt) {
            var i, $slide;
            var absDx = Math.abs(evt.dx);
            var slider_width = Math.round(slider.$list.outerWidth() * (1 + (this.opts.slideMarginPercent / 100)));

            // нормализация
            if (absDx > slider_width) {
                var leftCount = Math.floor(absDx / slider_width);
                absDx = absDx % slider_width;
                drager.startPoint = evt.point;

                i = 0;
                $slide = slider.$currentSlide;
                while ($slide.length && (i++ < leftCount)) {
                    $slide.css({
                        left: ''
                    });

                    $slide = slider.getNextSlide($slide);
                }

                slider.beforeSlide($slide);
                slider._setCurrentSlide($slide);
                slider.updateListHeight();
                slider.afterSlide($slide);
            }

            $slide = slider.$currentSlide;
            var $nextSlide = slider.getNextSlide($slide);

            var movePercent = absDx / slider_width;
            if (movePercent > 0.1) {
                var method = slider.getAnimationMethod(this.opts.animationName);
                if (method) {
                    method(slider, that.drager, evt);
                }

                this.slideTo(slider, $nextSlide, true);
            } else {
                // move
                $slide.css({
                    left: -absDx
                });
                $nextSlide.css({
                    left: -absDx + slider_width
                });
            }
        };

        DragPlugin.prototype.dragRight = function(slider, evt) {

        };

        return DragPlugin;
    })(SliderPlugin);

})(jQuery);
