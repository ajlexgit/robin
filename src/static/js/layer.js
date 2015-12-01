(function() {

    /*
        Эффект параллакса при скролле.

        Требует:
            jquery.utils.js, media_intervals.js

        Параметры:
            speed           - отношение пути перемещения блока к пути скролла
            strategy        - стратегия перемещения блока (top / transform)
            minEnabledWidth - минимальная ширина экрана, при которой блок перемещается
     */

    var $window = $(window);
    var layers = [];

    window.Layer = Class(null, function(cls, superclass) {
        cls.init = function(block, options) {
            this.$block = $(block).first();
            if (!this.$block.length) {
                console.error('Layer: block not found');
                return false;
            }

            // настройки
            this.opts = $.extend({
                speed: 0.5,
                strategy: 'top',
                minEnabledWidth: 768
            }, options);

            if ((this.opts.strategy != 'top') && (this.opts.strategy != 'transform')) {
                console.error('Layer: undefined strategy');
                return false;
            }

            // отвязывание старого экземпляра
            var old_instance = this.$block.data(cls.dataParamName);
            if (old_instance) {
                old_instance.destroy();
            }

            // получаем начальное положение
            if (this.opts.strategy == 'top') {
                this._initial = parseInt(this.$block.css('top')) || 0;
            } else {
                var matrix = this.$block.css('transform');
                var match = /(\d+)\)/.exec(matrix);
                if (match) {
                    this._initial = parseInt(match[1]) || 0;
                } else {
                    this._initial = 0;
                }
            }

            // интервал ширины окна, на котором модуль включен
            var that = this;
            this._media_interval = MediaInterval.create(this.opts.minEnabledWidth, 0);
            this._media_interval.enter(function() {
                that.enable()
            }).leave(function() {
                that.disable()
            });

            // включаем, если интервал активен
            if (this._media_interval.is_active()) {
                this.enable();
            }

            // Сохраняем объект в массив для использования в событиях
            layers.push(this);

            this.$block.data(cls.dataParamName, this);
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.disable();
            this._media_interval.destroy();
            this.$block.removeData(cls.dataParamName);

            var index = layers.indexOf(this);
            if (index >= 0) {
                layers.splice(index, 1);
            }
        };

        /*
            Включение параллакса
         */
        cls.prototype.enable = function() {
            if (this._enabled) {
                return
            } else{
                this._enabled = true;
            }

            this.process();
        };

        /*
            Отключение параллакса
         */
        cls.prototype.disable = function() {
            if (!this._enabled) {
                return
            } else {
                this._enabled = false;
            }

            if (this.opts.strategy == 'top') {
                this.$block.css('top', this._initial);
            } else {
                this.$block.css('transform', 'translateY(' + this._initial + 'px)');
            }
        };

        /*
            Расчет смещения картинки по текущему положению окна
         */
        cls.prototype.process = function(win_scroll) {
            if (!this._enabled) {
                return
            }

            win_scroll = win_scroll || $window.scrollTop();

            var delta = this._initial + parseInt(this.opts.speed * win_scroll);
            if (this.opts.strategy == 'top') {
                this.$block.css('top', delta + 'px');
            } else {
                this.$block.css('transform', 'translateY(' + delta + 'px)');
            }
        };
    });
    Layer.dataParamName = 'layer';


    /*
        Применение положения всех блоков
     */
    var updateLayers = function() {
        var win_scroll = $window.scrollTop();

        $.each(layers, function(i, item) {
            $.animation_frame(function() {
                item.process(win_scroll);
            })(item.$block.get(0));
        });
    };

    $window.on('scroll.layers', updateLayers);
    $window.on('load.layers', updateLayers);

    $.fn.layer = function(options) {
        return this.each(function() {
            Layer.create(this, options);
        })
    }

})(jQuery);
