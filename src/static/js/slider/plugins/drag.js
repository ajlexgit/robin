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
                ignoreDistance: 10,

                minSlidePercent: 20
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
                    var method = slider.getAnimationMethod(that.opts.animationName, 'dragStart');
                    if (method) {
                        method(slider, that, evt);
                    }
                },
                onDrag: function(evt) {
                    var method = slider.getAnimationMethod(that.opts.animationName, 'drag');
                    if (method) {
                        method(slider, that, evt);
                    }
                },
                onStopDrag: function(evt) {
                    var method = slider.getAnimationMethod(that.opts.animationName, 'dragStop');
                    if (method) {
                        method(slider, that, evt);
                    }
                }
            })
        };

        return DragPlugin;
    })(SliderPlugin);

})(jQuery);
