(function() {
    'use strict';

    /*
        Параллакс-эффект для блока.
        Блок должен иметь position, отличный от static.

        Требует:
            jquery.utils.js, bg_inspector.js, media_inspector.js

        Параметры:
            selector        - селектор выбора элемента, который будет перемещаться
            easing          - функция сглаживания перемещения фона
            bgHeight        - высота фоновой картинки в процентах относительно высоты блока (>= 100)
            minEnabledWidth - минимальная ширина экрана, при которой элемент перемещается

            onInit          - функция, выполняемая после инициализации объекта.
            onDisable       - функция, выполняемая при отключении плагина

        События:
            // Инициализация объекта
            init

        Пример:
            <div id="block">
                <img class="parallax" src="/img/bg.jpg">
                ...
            </div>

            $(document).ready(function() {
                Parallax('#block');

                // или

                $('#block').parallax();
            });
     */

    var $window = $(window);
    var parallaxes = [];

    window.Parallax = Class(EventedObject, function Parallax(cls, superclass) {
        cls.defaults = {
            selector: '.parallax',
            easing: 'easeInOutQuad',
            bgHeight: 150,
            minEnabledWidth: 768,

            onInit: $.noop,
            onDisable: $.noop
        };

        cls.DATA_KEY = 'parallax';


        cls.init = function(block, options) {
            superclass.init.call(this);

            this.$block = $(block).first();
            if (!this.$block.length) {
                return this.raise('block not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);
            if (this.opts.bgHeight < 100) {
                return this.raise('bgHeight should not be less than 100');
            }

            // передвигающийся элемент
            this.$bg = this.$block.find(this.opts.selector);
            if (!this.$bg.length) {
                return this.raise('background not found');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$block.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            this.$block.css({
                overflow: 'hidden'
            });

            // Сохраняем объект в массив для использования в событиях
            parallaxes.push(this);

            this.$block.data(this.DATA_KEY, this);
            this.opts.onInit.call(this);
            this.trigger('init');

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

            // инспектирование пропорций
            $.bgInspector.inspect(this.$bg, {
                checkOnInit: false,
                afterCheck: function($element, opts, state) {
                    if (state) {
                        // картинка шире
                        if (that._enabled) {
                            $element.css({
                                width: '',
                                height: that.opts.bgHeight + '%'
                            })
                        } else {
                            $element.css({
                                width: '',
                                height: '100.5%'
                            })
                        }
                    } else {
                        // картинка выше
                        if (that._enabled) {
                            var $parent = $element.parent();
                            var elem_asp = $element.data('bginspector_aspect');
                            var parent_asp = $parent.data('bginspector_aspect');

                            var relation = 100 * (parent_asp / elem_asp);
                            if (relation > that.opts.bgHeight) {
                                $element.css({
                                    width: '100.5%',
                                    height: ''
                                })
                            } else {
                                $element.css({
                                    width: 100 * that.opts.bgHeight / relation + '%',
                                    height: ''
                                })
                            }
                        } else {
                            $element.css({
                                width: '100.5%',
                                height: ''
                            })
                        }
                    }
                }
            });

            // Вызов инспектора после загрузки картинки
            this.$bg.onLoaded(true, function() {
                var $image = $(this);
                $image.css('display', 'inline-block');
                $.bgInspector.check($image);
            });
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.disable();
            $.bgInspector.ignore(this.$bg);
            $.mediaInspector.ignore(this.$block);
            this.$block.removeData(this.DATA_KEY);

            var index = parallaxes.indexOf(this);
            if (index >= 0) {
                parallaxes.splice(index, 1);
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

            this.$bg.css({
                transform: 'translate(-50%, 0)',
                minHeight: this.opts.bgHeight + '%'
            });

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

            this.$bg.css({
                transform: '',
                minHeight: '',
                top: ''
            });

            this.opts.onDisable.call(this);
        };

        /*
            Расчет смещения картинки по текущему положению окна
         */
        cls.process = function(win_scroll, win_height) {
            if (!this._enabled) {
                return
            }

            win_scroll = win_scroll || $window.scrollTop();
            win_height = win_height || $window.height();

            var block_top = this.$block.offset().top;
            var block_height = this.$block.outerHeight();
            var scrollFrom = block_top - win_height;
            var scrollTo = block_top + block_height;
            if ((win_scroll < scrollFrom) || (win_scroll > scrollTo)) {
                return
            }

            var scrollLength = scrollTo - scrollFrom;
            var scrollPosition = (win_scroll - scrollFrom) / scrollLength;

            var eProgress = $.easing[this.opts.easing](scrollPosition);
            var backgroundOffset = eProgress * (this.opts.bgHeight - 100);

            this.$bg.css({
                top: -backgroundOffset + '%'
            });
        };
    });


    var applyParallaxes = function() {
        var win_scroll = $window.scrollTop();
        var win_height = $window.height();

        $.each(parallaxes, function(i, item) {
            $.animation_frame(function() {
                item.process(win_scroll, win_height);
            })(item.$bg.get(0));
        });
    };

    $window.on('scroll.parallax', applyParallaxes);
    $window.on('load.parallax', applyParallaxes);
    $window.on('resize.parallax', $.rared(applyParallaxes, 100));

    $.fn.parallax = function(options) {
        return this.each(function() {
            window.Parallax(this, options);
        })
    }

})(jQuery);
