(function() {

    /*
        Эффект параллакса при скролле.

        Требует:
            jquery.utils.js
     */

    var $window = $(window);
    var layers = [];

    window.Layer = (function() {
        var Layer = function(block, options) {
            this.$block = $.findFirstElement(block);
            if (!this.$block.length) {
                console.error('Layer can\'t find block');
                return
            }

            // настройки
            this.opts = $.extend(true, this.getDefaultOpts(), options);

            this._start = 0;
            if (this.opts.strategy == 'top') {
                this._start = parseInt(this.$block.css('top'));
            } else if (this.opts.strategy == 'marginTop') {
                this._start = parseInt(this.$block.css('marginTop'));
            }

            // включение
            if (window.innerWidth >= this.opts.minEnableWidth) {
                this.enable()
            }

            // Сохраняем объект в массив для использования в событиях
            layers.push(this);
        };

        Layer.prototype.getDefaultOpts = function() {
            return {
                speed: 0.5,
                strategy: 'marginTop',     //  top / transform
                minEnableWidth: 768
            }
        };

        /*
            Включение параллакса
         */
        Layer.prototype.enable = function() {
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
        Layer.prototype.disable = function() {
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
        Layer.prototype.process = function(win_scroll) {
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

        return Layer;
    })();


    var applyParallaxes = function() {
        var win_scroll = $window.scrollTop();

        $.each(layers, function(i, obj) {
            $.animation_frame(function() {
                obj.process(win_scroll);
            })(obj.$block.get(0));
        });
    };

    $window.on('scroll.layers', applyParallaxes);
    $window.on('load.layers', applyParallaxes);
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
        this.each(function() {
            new Layer(this, options);
        })
    }

})(jQuery);
