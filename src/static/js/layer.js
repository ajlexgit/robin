(function() {
    'use strict';

    /*
        Эффект параллакса, зависящий от величины прокрутки страницы.

        Требует:
            jquery.utils.js, media_inspector.js

        Параметры:
            strategy        - стратегия перемещения блока (top / transform)
            minEnabledWidth - минимальная ширина экрана, при которой блок перемещается

            onInit          - функция, выполняемая после инициализации объекта.
            calcOffset      - функция, рассчитывающая смещение блока.
                              Если вернет false - блок останется на месте.

        События:
            // Инициализация объекта
            init

        Пример:
            // Двигаем блок внутри контейнера #ctnr.
            // Перемещение начинается от точки, когда контейнер становится видимым

            $('.layer').layer({
                onInit: function() {
                    this.$ctnr = $('#ctnr');
                },
                calcOffset: function(win_scroll) {
                    var ctnr_top = this.$ctnr.offset().top;
                    var ctnr_height = this.$ctnr.outerHeight();
                    var win_height = document.documentElement.clientHeight;

                    var from_point = ctnr_top - win_height;
                    var to_point = ctnr_top + ctnr_height;

                    if ((win_scroll >= from_point) && (win_scroll <= to_point)) {
                        return this._initial + parseInt(0.5 * (win_scroll - from_point));
                    } else {
                        return false;
                    }
                }
            })

     */

    var $window = $(window);
    var layers = [];

    window.Layer = Class(EventedObject, function Layer(cls, superclass) {
        cls.STRATEGY_TOP = 'top';
        cls.STRATEGY_TRANSFORM = 'transform';
        cls.STRATEGIES = [
            cls.STRATEGY_TOP,
            cls.STRATEGY_TRANSFORM
        ];

        cls.defaults = {
            strategy: cls.STRATEGY_TOP,
            minEnabledWidth: 768,

            onInit: $.noop,
            calcOffset: function(win_scroll) {
                return this._initial + parseInt(0.5 * win_scroll)
            }
        };

        cls.DATA_KEY = 'layer';


        cls.init = function(block, options) {
            superclass.init.call(this);

            this.$block = $(block).first();
            if (!this.$block.length) {
                return this.raise('block not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);
            if (cls.STRATEGIES.indexOf(this.opts.strategy) < 0) {
                return this.raise('undefined strategy');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$block.data(this.DATA_KEY);
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

            // Включение и выключение параллакса в зависимости
            // от ширины окна браузера
            var that = this;
            $.mediaInspector.inspect(this.$block, {
                point: that.opts.minEnabledWidth,
                afterCheck: function($block, opts, state) {
                    var old_state = this.getState($block);
                    if (state === old_state) {
                        return
                    }

                    if (state) {
                        that.enable();
                    } else {
                        that.disable()
                    }
                }
            });

            // Сохраняем объект в массив для использования в событиях
            layers.push(this);

            this.$block.data(this.DATA_KEY, this);

            this.opts.onInit.call(this);
            this.trigger('init');

            $.mediaInspector.check(this.$block);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.disable();
            $.mediaInspector.ignore(this.$block);
            this.$block.removeData(this.DATA_KEY);

            var index = layers.indexOf(this);
            if (index >= 0) {
                layers.splice(index, 1);
            }

            superclass.destroy.call(this);
        };

        /*
            Включение параллакса
         */
        cls.enable = function() {
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
        cls.disable = function() {
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
        cls.process = function(win_scroll) {
            if (!this._enabled) {
                return
            }

            win_scroll = win_scroll || $window.scrollTop();

            // рассчет смещения
            var offset = this.opts.calcOffset.call(this, win_scroll);
            if (offset === false) {
                return
            }

            if (this.opts.strategy == 'top') {
                this.$block.css('top', offset + 'px');
            } else {
                this.$block.css('transform', 'translateY(' + offset + 'px)');
            }
        };
    });


    /*
        Обновление положения всех блоков
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
            window.Layer(this, options);
        })
    }

})(jQuery);
