(function() {

    /*
        Эффект параллакса при скролле.

        Требует:
            jquery.utils.js

        Параметры:
            speed           - отношение пути перемещения блока к пути скролла
            strategy        - стратегия перемещения блока (margin / top)
            minEnableWidth  - минимальная ширина экрана, при которой блок перемещается
     */

    var $window = $(window);
    var layers = [];

    window.Layer = Class(null, function(cls, superclass) {
        var dataParamName = 'layer';

        cls.init = function(block, options) {
            this.$block = $(block).first();
            if (!this.$block.length) {
                console.error('Layer can\'t find block');
                return false;
            } else {
                // отвязывание старого экземпляра
                var old_instance = this.$block.data(dataParamName);
                if (old_instance) {
                    old_instance.destroy();
                }
                this.$block.data(dataParamName, this);
            }

            // настройки
            this.opts = $.extend({
                speed: 0.5,
                strategy: 'top',
                minEnableWidth: 768
            }, options);

            // получаем начальное положение
            this._start = 0;
            if (this.opts.strategy == 'top') {
                this._start = parseInt(this.$block.css('top')) || 0;
            } else if (this.opts.strategy == 'margin') {
                this._start = parseInt(this.$block.css('margin')) || 0;
            }

            // включение
            if (window.innerWidth >= this.opts.minEnableWidth) {
                this.enable();
            }

            // Сохраняем объект в массив для использования в событиях
            layers.push(this);
        };

        /*
            Отвязывание плагина
         */
        cls.prototype.destroy = function() {
            this.disable();
            this.$block.removeData(dataParamName);

            var index = layers.indexOf(this);
            if (index >= 0) {
                layers.splice(index, 1);
            }
        };

        /*
            Включение параллакса
         */
        cls.prototype.enable = function() {
            if (this.enabled) {
                return
            } else{
                this.enabled = true;
            }

            this.process();
        };

        /*
            Отключение параллакса
         */
        cls.prototype.disable = function() {
            if (!this.enabled) {
                return
            } else {
                this.enabled = false;
            }

            if (!this._start) {
                this.$block.css(this.opts.strategy, '');
            } else {
                if (this.opts.strategy == 'transform') {
                    this.$block.css(this.opts.strategy, 'translateY(' + this._start + 'px)');
                } else {
                    this.$block.css(this.opts.strategy, this._start);
                }
            }
        };

        /*
            Расчет смещения картинки по текущему положению окна
         */
        cls.prototype.process = function(win_scroll) {
            if (!this.enabled) {
                return
            }

            win_scroll = win_scroll || $window.scrollTop();

            var delta = this._start + parseInt(this.opts.speed * win_scroll);
            if (this.opts.strategy == 'transform') {
                this.$block.css('transform', 'translateY(' + delta + 'px)');
            } else {
                this.$block.css(this.opts.strategy, delta + 'px');
            }
        };
    });


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
    $window.on('resize.layers', $.rared(function() {
        $.each(layers, function() {
            if (window.innerWidth < this.opts.minEnableWidth) {
                this.disable()
            } else {
                this.enable()
            }
        });
    }, 100));


    $.fn.layer = function(options) {
        return this.each(function() {
            Layer.create(this, options);
        })
    }

})(jQuery);
