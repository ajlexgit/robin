(function() {
    'use strict';

    /*
        Эффект параллакса, зависящий от величины прокрутки страницы.

        Требует:
            jquery.utils.js, media_inspector.js

        Параметры:
            selector        - селектор элементов, которые будут перемещаться
            strategy        - стратегия перемещения блока (top / transform)
            minEnabledWidth - минимальная ширина экрана, при которой блок перемещается

            onInit          - функция, выполняемая после инициализации объекта.
            onDisable       - функция, выполняемая при отключении плагина
            beforeCalc      - функция, выполняемая перед расчетом смещения. Если вернёт false - блок не сдвинется
            calcOffset      - функция, рассчитывающая смещение блока.
                              Если вернет false - блок останется на месте.

        Пример:
            // Двигаем блок внутри контейнера #ctnr.
            // Перемещение начинается от точки, когда контейнер становится видимым

            $('.layer').layer({
                selector: '.item',
                calcOffset: function($item, params) {
                    var percentage = (params.scroll - params.from_point) / (params.to_point - params.from_point);
                    return percentage * (params.win_height - $item.height());
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
            selector: 'img',
            strategy: cls.STRATEGY_TRANSFORM,
            minEnabledWidth: 768,

            onInit: $.noop,
            beforeCalc: function(params) {
                params.root_top = this.$root.offset().top;
                params.root_height = this.$root.outerHeight();
                params.win_height = $.winHeight();

                params.from_point = params.root_top - params.win_height;
                params.to_point = params.root_top + params.root_height;
                if ((params.scroll < params.from_point) || (params.scroll > params.to_point)) {
                    return false
                }
            },
            calcOffset: function($item, params) {
                return parseInt(0.5 * params.scroll)
            },
            onDisable: function() {
                if (this.opts.strategy == 'top') {
                    this.$items.css('top', '');
                } else {
                    this.$items.css('transform', '');
                }
            }
        };


        cls.init = function(element, options) {
            superclass.init.call(this);

            this.$root = $(element).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);
            if (cls.STRATEGIES.indexOf(this.opts.strategy) < 0) {
                return this.raise('undefined strategy');
            }

            this.$items = this.$root.find(this.opts.selector);
            if (!this.$items.length) {
                return this.raise('items not found');
            }

            // Сохраняем объект в массив для использования в событиях
            layers.push(this);
            this.opts.onInit.call(this);

            // Включение и выключение параллакса в зависимости
            // от ширины окна браузера
            var that = this;
            $.mediaInspector.inspect(this.$root, {
                point: that.opts.minEnabledWidth,
                afterCheck: function($root, opts, state) {
                    var old_state = this.getState($root);
                    if (state === old_state) {
                        return
                    }

                    if (state) {
                        that.enable();
                    } else {
                        that.disable();
                    }
                }
            });
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.disable();
            $.mediaInspector.ignore(this.$root);

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

            this.opts.onDisable.call(this);
        };

        /*
            Расчет смещения элемента по текущему положению окна
         */
        cls.process = function(win_scroll) {
            if (!this._enabled) {
                return
            }

            var params = {
                scroll: win_scroll || $window.scrollTop()
            };

            // ограничение областью видимости блока
            if (this.opts.beforeCalc.call(this, params) === false) {
                return
            }

            // рассчет смещения
            var that = this;
            this.$items.each(function() {
                var $item = $(this);
                var offset = that.opts.calcOffset.call(that, $item, params);
                if (offset === false) {
                    return
                }

                if (that.opts.strategy == 'top') {
                    $item.css('top', offset + 'px');
                } else {
                    $item.css('transform', 'translateY(' + offset + 'px)');
                }
            });
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
            })(item.$root.get(0));
        });
    };

    $window.on('scroll.layers', updateLayers);
    $window.on('load.layers', updateLayers);
    $window.on('resize.layers', $.rared(updateLayers, 100));

    $.fn.layer = function(options) {
        return this.each(function() {
            window.Layer(this, options);
        })
    }

})(jQuery);
