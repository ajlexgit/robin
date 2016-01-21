(function($) {

    /*
        Модуль слайдера с подключаемыми плагинами.

        Требует:
            jquery.utils.js

        Параметры:
            rootClass                       - класс, добавляемый корневому элементу
            listWrapperClass                - класс, добавляемый обертке над списком
            listClass                       - класс, добавляемый списку
            slideClass                      - класс, добавляемый слайду
            itemClass                       - класс, добавляемый элементу списка

            initialActiveClass              - класс начально активного элемента
            setItemsPerSlideAnimationName   - анимация выбора текущего слайда при изменении кол-ва
                                              элементов в каждом слайде
            setItemsPerSlideAnimatedHeight  - анимировать или нет высоту слайдера при изменении
                                              кол-ва элементов в каждом слайде

            itemSelector                    - селектор элементов списка
            itemsPerSlide                   - кол-во элментов на каждый слайд (может быть функцией)
            loop                            - зациклить слайдер
            adaptiveHeight                  - менять высоту слайдера в зависимости от высоты
                                              текущего слайда
            adaptiveHeightTransition        - длительность анимации высоты слайдера

            onInit                          - событие инициализации
            onSetItemsPerSlide              - событие установки кол-ва элементов слайда
            onResize                        - событие изменения размера окна

        HTML input:
            <div id="slider">
                <img class="slide">
                <img class="slide">
                ...
            </div>

        JS пример:
            Slider('#slider', {
                loop: false,
                adaptiveHeight: true,
                adaptiveHeightTransition: 800,
                itemsPerSlide: 2
            }).attachPlugins([
                SliderSideAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                SliderSideShortestAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                SliderFadeAnimation({
                    speed: 800
                }),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin({
                    animationName: 'side'
                }),
                SliderDragPlugin({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 3000
                })
            ]);
    */

    var sliders = [];

    window.Slider = Class(null, function Slider(cls, superclass) {
        cls.defaults = {
            rootClass: 'slider-root',
            listWrapperClass: 'slider-list-wrapper',
            listClass: 'slider-list',
            slideClass: 'slider-slide',
            itemClass: 'slider-item',

            initialActiveClass: 'active',
            setItemsPerSlideAnimationName: 'instant',
            setItemsPerSlideAnimatedHeight: false,

            itemSelector: '.slide',
            itemsPerSlide: 1,
            loop: true,
            adaptiveHeight: true,
            adaptiveHeightTransition: 800,

            onInit: $.noop,
            onSetItemsPerSlide: $.noop,
            onResize: $.noop
        };

        cls.DATA_KEY = 'slider';


        cls.init = function(list, options) {
            this.$list = $(list).first();
            if (!this.$list.length) {
                return this.raise('list element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // плагины
            this._plugins = [
                SliderInstantAnimation()
            ];

            // добавляем класс на список
            this.$list.addClass(this.opts.listClass);

            // создание обертки списка
            this.$list.wrap('<div>');
            this.$listWrapper = this.$list.parent().addClass(this.opts.listWrapperClass);

            // создание корневого элемента слайдера
            this.$listWrapper.wrap('<div>');
            this.$root = this.$listWrapper.parent().addClass(this.opts.rootClass);


            // сохраняем массив items
            this.$items = this.$list.find(this.opts.itemSelector);
            this.$items.addClass(this.opts.itemClass);

            if (!this.$items.length) {
                return this.raise('there are no items in list');
            }

            // флаг анимации и объект анимации
            this._animated = false;
            this._animation = null;

            // текущий элемент
            this.$currentItem = this.$items.filter('.' + this.opts.initialActiveClass).first();
            if (!this.$currentItem.length) {
                this.$currentItem = this.$items.first();
            }

            // создаем слайды
            this.setItemsPerSlide(this.opts.itemsPerSlide);

            // обновление высоты по мере загрузки картинок
            if (this.opts.adaptiveHeight) {
                var $images = this.$currentSlide.find('img');
            } else {
                $images = this.$list.find('img');
            }

            var that = this;
            var loadHandle = $.rared(function() {
                that.updateListHeight();
            }, 100);

            $images.on('load', loadHandle);

            // callback
            this.opts.onInit.call(this);

            this.$list.data(this.DATA_KEY, this);

            sliders.push(this);
        };

        // ===============================================
        // ================ current slide ================
        // ===============================================

        /*
            Получение активного слайда
         */
        cls.getCurrentSlide = function() {
            return this.$currentItem.closest('.' + this.opts.slideClass);
        };

        /*
            Изменение текущего слайда
         */
        cls.setCurrentSlide = function($slide) {
            if (!$slide || !$slide.length || (this.$slides.index($slide) < 0)) {
                return false
            }

            if (this.$currentSlide && (this.$currentSlide.get(0) == $slide.get(0))) {
                return false
            }

            this.beforeSetCurrentSlide($slide);
            this.$currentItem = $slide.find('.' + this.opts.itemClass).first();
            this.$currentSlide = $slide;
            this.afterSetCurrentSlide($slide);

            return $slide;
        };

        cls.beforeSetCurrentSlide = function($slide) {
            // jQuery event
            this.$list.trigger('beforeSetCurrentSlide.slider', [$slide]);

            this.callPluginsMethod('beforeSetCurrentSlide', [$slide]);
        };

        cls.afterSetCurrentSlide = function($slide) {
            this.callPluginsMethod('afterSetCurrentSlide', [$slide], true);

            // jQuery event
            this.$list.trigger('afterSetCurrentSlide.slider', [$slide]);
        };

        // ===============================================
        // ================ create slides ================
        // ===============================================

        /*
            Создание слайдов, содержащих по itemsPerSlide элементов
            в каждом слайде.

            В каждом плагине вызывает методы beforeSetItemsPerSlide и afterSetItemsPerSlide
         */
        cls.setItemsPerSlide = function(itemsPerSlide) {
            // Прерывание анимации, если она запущена
            if (this._animated && this._animation) {
                this._animation.stop(true)
            }

            // если функция
            if ($.isFunction(itemsPerSlide)) {
                itemsPerSlide = parseInt(itemsPerSlide.call(this));
            }
            itemsPerSlide = parseInt(itemsPerSlide);
            if (!itemsPerSlide) {
                return
            }

            this.beforeSetItemsPerSlide(itemsPerSlide);

            // удаляем ранее созданные слайды
            this.$slides = $();
            this.$list.find('.' + this.opts.slideClass).remove();

            // создаем слайды
            var slide_count = Math.ceil(this.$items.length / itemsPerSlide);
            for (var i = 0; i < slide_count; i++) {
                var $slide = $('<div>');
                this.$list.append(
                    $slide.append(
                        this.$items.slice(i * itemsPerSlide, (i + 1) * itemsPerSlide)
                    )
                );
                this.$slides.push($slide.get(0));
            }

            // добавляем слайдам класс
            this.$slides.addClass(this.opts.slideClass);

            // переход к активному слайду
            this.slideTo(
                this.getCurrentSlide(),
                this.opts.setItemsPerSlideAnimationName,
                this.opts.setItemsPerSlideAnimatedHeight
            );

            this.afterSetItemsPerSlide(itemsPerSlide);

            // callback
            this.opts.onSetItemsPerSlide.call(this, itemsPerSlide);
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед созданием слайдов.
         */
        cls.beforeSetItemsPerSlide = function(itemsPerSlide) {
            // jQuery event
            this.$list.trigger('beforeSetItemsPerSlide.slider');

            this.callPluginsMethod('beforeSetItemsPerSlide');
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после созданием слайдов.
         */
        cls.afterSetItemsPerSlide = function(itemsPerSlide) {
            this.callPluginsMethod('afterSetItemsPerSlide', null, true);

            // jQuery event
            this.$list.trigger('afterSetItemsPerSlide.slider');
        };

        // ===============================================
        // =============== slides methods ================
        // ===============================================

        /*
            Метод, возвращающий следующий слайд. Возможно указать количество
            слайдов, которые нужно пропустить.
         */
        cls.getNextSlide = function($fromSlide, passCount) {
            if (!$fromSlide || !$fromSlide.length) {
                $fromSlide = this.$currentSlide;
            }

            passCount = passCount || 0;
            var slides_count = this.$slides.length;
            var index = this.$slides.index($fromSlide) + (passCount || 0) + 1;

            if (this.opts.loop) {
                return this.$slides.eq(index % slides_count);
            } else if (index < slides_count) {
                return this.$slides.eq(index);
            }

            return $();
        };

        /*
            Метод, возвращающий предыдущий слайд. Возможно указать количество
            слайдов, которые нужно пропустить.
         */
        cls.getPreviousSlide = function($fromSlide, passCount) {
            if (!$fromSlide || !$fromSlide.length) {
                $fromSlide = this.$currentSlide;
            }

            var slides_count = this.$slides.length;
            var index = this.$slides.index($fromSlide) - (passCount || 0) - 1;

            if (this.opts.loop) {
                return this.$slides.eq(index % slides_count);
            } else if (index >= 0) {
                return this.$slides.eq(index);
            }

            return $();
        };

        // ===============================================
        // ============== plugin methods =================
        // ===============================================

        /*
            Добавление текущего объекта к массиву аргументов.
         */
        cls._argsWithThis = function(args) {
            var final_args = args || [];
            final_args = Array.prototype.slice.call(final_args);
            final_args.unshift(this);
            return final_args;
        };

        /*
            Подключение плагинов
         */
        cls.attachPlugins = function(plugins) {
            if ($.isArray(plugins)) {
                for (var i = 0; i < plugins.length; i++) {
                    var plugin = plugins[i];
                    if (plugin && (plugin instanceof SliderPlugin)) {
                        this._plugins.push(plugin);
                        plugin.onAttach(this);
                        plugin.afterAttach(this);
                    }
                }
            } else if (plugins && (plugins instanceof SliderPlugin)) {
                this._plugins.push(plugins);
                plugins.onAttach(this);
                plugins.afterAttach(this);
            }
            return this;
        };

        /*
            Поиск реализации метода анимации среди плагинов
         */
        cls.getAnimationMethod = function(animationName, methodName) {
            methodName = methodName || 'slideTo';
            var index = this._plugins.length;
            while (index--) {
                var plugin = this._plugins[index];
                if ((methodName in plugin) && (plugin.opts.name == animationName)) {
                    return $.proxy(plugin[methodName], plugin);
                }
            }

            this.warn('Not found method "' + methodName + '" with name "' + animationName + '"');
        };

        /*
            Вызом метода methodName с агрументами [slider, *additionArgs] во всех плагинах,
            в которых этот метод реализован.

            Первым аргументом ВСЕГДА стоит slider, независимо от значения additionArgs.

            Если reversed=true, обход плагинов будет в обратном порядке
            (от поключенных первыми)
         */
        cls.callPluginsMethod = function(methodName, additionArgs, reversed) {
            var plugins = this._plugins.concat();
            if (reversed) {
                plugins.reverse();
            }

            var final_args = this._argsWithThis(additionArgs);
            var index = plugins.length;
            while (index--) {
                var plugin = plugins[index];
                if (methodName in plugin) {
                    plugin[methodName].apply(plugin, final_args);
                }
            }
        };

        // ===============================================
        // ================= update height ===============
        // ===============================================

        /*
            Рассчет финальной высоты слайдера
         */
        cls.calcListHeight = function() {
            if (this.opts.adaptiveHeight) {
                return this.$currentSlide.outerHeight();
            }

            var final_height = 0;
            this.$slides.height('auto');
            $.each(this.$slides, function(i, slide) {
                var $slide = $(slide);
                var height = $slide.outerHeight();
                if (height > final_height) {
                    final_height = height;
                }
            });
            this.$slides.height('');
            return final_height;
        };

        /*
            Обновление высоты slider.$list в зависимости от высоты слайдов
            и настройки adaptiveHeight
         */
        cls.updateListHeight = function(animatedHeight) {
            // прерываем анимация высоты, если она идёт
            if (this._adaptive_animation) {
                this._adaptive_animation.stop();
            }

            var final_height = this.calcListHeight();
            var current_height = this.$list.outerHeight();

            // высота не меняется - выходим
            if (current_height == final_height) {
                return
            }

            this.beforeUpdateListHeight(current_height, final_height);
            if (animatedHeight && this.opts.adaptiveHeightTransition) {
                // с анимацией
                var that = this;
                this._adaptive_animation = $.animate({
                    duration: this.opts.adaptiveHeightTransition,
                    delay: 40,
                    easing: 'easeOutCubic',
                    init: function() {
                        this.autoInit('height', current_height, final_height);
                    },
                    step: function(eProgress) {
                        var height = this.autoCalc('height', eProgress);
                        $.animation_frame(function() {
                            that.$list.outerHeight(height);
                        }, that.$list.get(0))();
                    }
                })
            } else {
                // мгновенно
                this.$list.outerHeight(final_height);
            }
            this.afterUpdateListHeight(current_height, final_height);
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед обновлением высоты списка.
         */
        cls.beforeUpdateListHeight = function(current, final) {
            // jQuery event
            this.$list.trigger('beforeUpdateListHeight.slider', arguments);

            this.callPluginsMethod('beforeUpdateListHeight', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после обновления высоты списка.
         */
        cls.afterUpdateListHeight = function(current, final) {
            this.callPluginsMethod('afterUpdateListHeight', arguments, true);

            // jQuery event
            this.$list.trigger('afterUpdateListHeight.slider', arguments);
        };


        // ===============================================
        // =============== slide animation ===============
        // ===============================================

        /*
            Метод смены текущего слайда на $toSlide.

            В реализации этого метода НЕОБХОДИМО вызывать методы слайдера
            beforeSlide и afterSlide:
                slider.beforeSlide($toSlide);
                ....
                slider.afterSlide($toSlide);

            Объект анимации (если он есть) НЕОБХОДИМО сохранить в переменной slider._animation
         */
        cls.slideTo = function($toSlide, animationName, animatedHeight) {
            if (!$toSlide || !$toSlide.length || (this.$slides.index($toSlide) < 0)) {
                return
            }

            // скролл к уже активному слайду
            if (this.$currentSlide && (this.$currentSlide.get(0) === $toSlide.get(0))) {
                return
            }

            animationName = animationName || 'instant';
            var method = this.getAnimationMethod(animationName);
            if (method) {
                method.call(null, this, $toSlide, animatedHeight);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед переходом к слайду.
         */
        cls.beforeSlide = function($toSlide) {
            // jQuery event
            this.$list.trigger('beforeSlide.slider', arguments);

            this.callPluginsMethod('beforeSlide', arguments);

            this._animated = true;
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после перехода к слайду.
         */
        cls.afterSlide = function($toSlide) {
            this._animated = false;

            this.callPluginsMethod('afterSlide', arguments, true);

            // jQuery event
            this.$list.trigger('afterSlide.slider', arguments);
        };

        cls.slideNext = function(animationName, animatedHeight) {
            var $next = this.getNextSlide();
            this.slideTo($next, animationName, animatedHeight);
        };

        cls.slidePrevious = function(animationName, animatedHeight) {
            var $prev = this.getPreviousSlide();
            this.slideTo($prev, animationName, animatedHeight);
        };
    });


    // ================================================
    //            Базовый класс плагина
    // ================================================
    window.SliderPlugin = Class(null, function SliderPlugin(cls, superclass) {
        cls.defaults = {
            afterAttach: $.noop,
            onResize: $.noop
        };


        cls.init = function(settings) {
            this.opts = $.extend(true, {}, this.defaults, settings);
        };

        // Инициализация
        cls.onAttach = function(slider) {

        };

        // Дополнительные действия после подключения
        cls.afterAttach = function(slider) {
            this.opts.afterAttach.call(this, slider);
        };

        // Событие изменения размера окна
        cls.onResize = function(slider) {
            this.opts.onResize.call(this, slider);
        };
    });


    // ================================================
    //          Плагин мгновенной анимации
    // ================================================
    window.SliderInstantAnimation = Class(SliderPlugin, function SliderInstantAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'instant'
        });


        /*
            Реализация метода перехода от одного слайда к другому
         */
        cls.slideTo = function(slider, $toSlide, animatedHeight) {
            if (slider._animated) {
                return
            }

            slider.beforeSlide($toSlide);
            slider.$slides.css({
                left: ''
            });
            $toSlide.css({
                left: '0'
            });
            slider.setCurrentSlide($toSlide);
            slider.afterSlide($toSlide);

            slider.updateListHeight(animatedHeight);
        };
    });

    // Обновление высоты слайдера
    $(window).on('load.slider', function() {
        $.each(sliders, function(i, slider) {
            slider.updateListHeight()
        });
    }).on('resize.slider', $.rared(function() {
        $.each(sliders, function(i, slider) {
            slider.opts.onResize.call(slider);
            slider.callPluginsMethod('onResize');
            slider.updateListHeight();
        });
    }, 100));

})(jQuery);
