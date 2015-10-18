(function($) {

    /*
        Модуль слайдера с подключаемыми плагинами.

        Требует:
            jquery.utils.js

        HTML input:
            <div id="slider-wrapper">
                <div id="slider">
                    <img class="slide">
                    <img class="slide">
                    ...
                </div>
            </div>

        JS пример:
            var slider = new Slider($elem, {
                loop: false,
                adaptiveHeight: true,
                adaptiveHeightTransition: 800,
                slideItems: 2
            }).attachPlugins([
                new SliderSideAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                new SliderSideShortestAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                new SliderFadeAnimation({
                    speed: 800
                }),
                new SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                new SliderNavigationPlugin({
                    animationName: 'side'
                }),
                new SliderDragPlugin({
                    speed: 800,
                    slideMarginPercent: 5
                }),
                new SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 3000
                })
            ]);
    */

    var sliders = [];

    window.Slider = (function() {
        var Slider = function(element, settings) {
            var $element = $.findFirstElement(element);
            if (!$element.length) {
                console.error('Empty root element for Slider');
                return
            }

            this._plugins = [
                new SliderInstantAnimation()
            ];
            this.$currentSlide = $();

            // настройки
            var defaults = this.getDefaultOpts();
            this.opts = $.extend(true, defaults, settings);

            // сохраняем ссылку на список
            this.$list = this._createList($element);
            this.$list.addClass(this.opts.listClass);

            // создание обертки списка
            this.$listWrapper = this._createListWrapper();
            this.$listWrapper.addClass(this.opts.listWrapperClass);

            // создание корневого элемента слайдера
            this.$root = this._createRoot();
            this.$root.addClass(this.opts.rootClass);
            this.$root.data('slider', this);
            sliders.push(this);

            // сохраняем массив items
            this.$items = this._createItems();
            this.$items.addClass(this.opts.itemClass);

            // создаем слайды
            this.setSlideItems(this.opts.slideItems);

            // активация текущего слайда
            var $startSlide = this._getStartSlide();
            this.slideTo($startSlide, this.opts.initialAnimationName, this.opts.initialAnimatedHeight);

            // обновление высоты по мере загрузки картинок
            if (this.opts.adaptiveHeight) {
                var $images = this.$currentSlide.find('img');
            } else {
                $images = this.$list.find('img');
            }

            // флаг анимации и объект анимации
            this._animated = false;
            this._animation = null;

            var that = this;
            var loadHandle = $.rared(function() {
                that.updateListHeight();
            }, 100);

            $images.one('load', loadHandle);
        };


        // ===============================================
        // =========== initialization methods ============
        // ===============================================

        // Метод, возвращающий объект настроек по умолчанию
        Slider.prototype.getDefaultOpts = function() {
            return {
                rootClass: 'slider-root',
                listClass: 'slider-list',
                listWrapperClass: 'slider-list-wrapper',
                slideClass: 'slider-slide',
                itemClass: 'slider-item',

                initialActiveClass: 'active',
                initialAnimationName: 'instant',
                initialAnimatedHeight: false,
                setSlideItemsAnimationName: 'instant',
                setSlideItemsAnimatedHeight: false,

                itemSelector: '.slide',
                slideItems: 1,
                loop: true,
                adaptiveHeight: true,
                adaptiveHeightTransition: 800,

                onResize: $.noop
            };
        };

        // Метод, возвращающий ссылку на объект-список
        Slider.prototype._createList = function($element) {
            return $element;
        };

        // Метод, возвращающий ссылку на объект-обертку списка
        Slider.prototype._createListWrapper = function() {
            this.$list.wrap('<div>');
            return this.$list.parent();
        };

        // Метод, возвращающий ссылку на объект-обертку слайдера
        Slider.prototype._createRoot = function() {
            this.$listWrapper.wrap('<div>');
            return this.$listWrapper.parent();
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype._createItems = function() {
            return this.$list.find(this.opts.itemSelector);
        };


        // ===============================================
        // ============== plugin methods =================
        // ===============================================

        /*
            Добавление текущего объекта к массиву аргументов.
         */
        Slider.prototype._argsWithThis = function(args) {
            var final_args = args || [];
            final_args = Array.prototype.slice.call(final_args);
            final_args.unshift(this);
            return final_args;
        };

        /*
            Подключение плагинов
         */
        Slider.prototype.attachPlugins = function(plugins) {
            if ($.isArray(plugins)) {
                for (var i = 0; i< plugins.length; i++) {
                    var plugin = plugins[i];
                    this._plugins.push(plugin);
                    plugin.onAttach(this);
                }
            } else {
                this._plugins.push(plugins);
                plugins.onAttach(this);
            }
            return this;
        };

        /*
            Поиск реализации метода анимации среди плагинов
         */
        Slider.prototype.getAnimationMethod = function(animationName, methodName) {
            methodName = methodName || 'slideTo';
            var index = this._plugins.length;
            while (index--) {
                var plugin = this._plugins[index];
                if ((methodName in plugin) && (plugin.opts.name == animationName)) {
                    return $.proxy(plugin[methodName], plugin);
                }
            }

            console.error('Not found method "' + methodName + '" with name "' + animationName + '"');
        };

        /*
            Вызом метода methodName с агрументами [slider, *additionArgs] во всех плагинах,
            в которых этот метод реализован.

            Первым аргументом ВСЕГДА стоит slider, независимо от значения additionArgs.

            Если reversed=true, обход плагинов будет в обратном порядке
            (от поключенных первыми)
         */
        Slider.prototype.callPluginsMethod = function(methodName, additionArgs, reversed) {
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
        // =============== slides methods ================
        // ===============================================

        // Метод, возвращающий начально активный слайд
        Slider.prototype._getStartSlide = function() {
            var $active = this.$items.filter('.' + this.opts.initialActiveClass);
            if ($active.length) {
                return $active.first().closest('.' + this.opts.slideClass);
            }
            return this.$slides.first();
        };

        /*
            Метод, возвращающий следующий слайд. Возможно указать количество
            слайдов, которые нужно пропустить.
         */
        Slider.prototype.getNextSlide = function($fromSlide, passCount) {
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
        Slider.prototype.getPreviousSlide = function($fromSlide, passCount) {
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
        // ================ current slide ================
        // ===============================================

        /*
            Изменение текущего слайда
         */
        Slider.prototype.setCurrentSlide = function($slide) {
            if (!$slide || !$slide.length || (this.$slides.index($slide) < 0)) {
                return false
            }

            if (this.$currentSlide && (this.$currentSlide.get(0) == $slide.get(0))) {
                return false
            }

            this.beforeSetCurrentSlide($slide);
            this.$currentSlide = $slide;
            this.afterSetCurrentSlide($slide);
            return $slide
        };

        Slider.prototype.beforeSetCurrentSlide = function($slide) {
            // jQuery event
            this.$list.trigger('beforeSetCurrentSlide.slider', [$slide]);

            this.callPluginsMethod('beforeSetCurrentSlide', [$slide]);
        };

        Slider.prototype.afterSetCurrentSlide = function($slide) {
            this.callPluginsMethod('afterSetCurrentSlide', [$slide], true);

            // jQuery event
            this.$list.trigger('afterSetCurrentSlide.slider' ,[$slide]);
        };

        // ===============================================
        // ================ create slides ================
        // ===============================================

        /*
            Создание слайдов, содержащих по slideItems элементов
            в каждом слайде.

            В каждом плагине вызывает методы beforeSetSlideItems и afterSetSlideItems
         */
        Slider.prototype.setSlideItems = function(slideItems) {
            // Прерывание анимации, если она запущена
            if (this._animated && this._animation) {
                this._animation.stop(true)
            }

            this.beforeSetSlideItems();

            var slide_count = Math.ceil(this.$items.length / slideItems);
            var $current_item = this.$currentSlide.find('.' + this.opts.itemClass + ':first');

            this.$slides = $();
            this.$list.find('.' + this.opts.slideClass).remove();
            for (var i = 0; i < slide_count; i++) {
                var $slide = $('<div>');
                this.$list.append(
                    $slide.append(
                        this.$items.slice(i * slideItems, (i + 1) * slideItems)
                    )
                );
                this.$slides.push($slide.get(0));
            }
            this.$slides.addClass(this.opts.slideClass);

            // сохранение количества элементов в слайде
            this.opts.slideItems = slideItems;

            // активация текущего слайда
            var $startSlide = $current_item.closest('.' + this.opts.slideClass);
            this.slideTo($startSlide, this.opts.setSlideItemsAnimationName, this.opts.setSlideItemsAnimatedHeight);

            this.afterSetSlideItems();
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед созданием слайдов.
         */
        Slider.prototype.beforeSetSlideItems = function() {
            // jQuery event
            this.$list.trigger('beforeSetSlideItems.slider');

            this.callPluginsMethod('beforeSetSlideItems');
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после созданием слайдов.
         */
        Slider.prototype.afterSetSlideItems = function() {
            this.callPluginsMethod('afterSetSlideItems', null, true);

            // jQuery event
            this.$list.trigger('afterSetSlideItems.slider');
        };


        // ===============================================
        // ================= update height ===============
        // ===============================================

        /*
            Обновление высоты slider.$list в зависимости от высоты слайдов
            и настройки adaptiveHeight
         */
        Slider.prototype.updateListHeight = function(animatedHeight) {
            var final_height = 0;
            var current_height = this.$list.outerHeight();

            // определение финальной высоты слайдера
            if (this.opts.adaptiveHeight) {
                final_height = this.$currentSlide.outerHeight();
            } else {
                this.$slides.height('auto');
                $.each(this.$slides, function(i, slide) {
                    var $slide = $(slide);
                    var height = $slide.outerHeight();
                    if (height > final_height) {
                        final_height = height;
                    }
                });
                this.$slides.height('');
            }

            // прерываем анимация высоты, если она идёт
            if (this._adaptive_animation) {
                this._adaptive_animation.stop();
            }

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
        Slider.prototype.beforeUpdateListHeight = function(current, final) {
            // jQuery event
            this.$list.trigger('beforeUpdateListHeight.slider', arguments);

            this.callPluginsMethod('beforeUpdateListHeight', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после обновления высоты списка.
         */
        Slider.prototype.afterUpdateListHeight = function(current, final) {
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

            Объект анимации (если он есть) НЕОБХОДИМО сохранить в переменной
            slider._animation.
         */
        Slider.prototype.slideTo = function($toSlide, animationName, animatedHeight) {
            if (!$toSlide || !$toSlide.length || (this.$slides.index($toSlide) < 0)) {
                return
            }

            // скролл к уже активному слайду
            if (this.$currentSlide.get(0) === $toSlide.get(0)) {
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
        Slider.prototype.beforeSlide = function($toSlide) {
            this._animated = true;

            // jQuery event
            this.$list.trigger('beforeSlide.slider', arguments);

            this.callPluginsMethod('beforeSlide', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после перехода к слайду.
         */
        Slider.prototype.afterSlide = function($toSlide) {
            this._animated = false;

            this.callPluginsMethod('afterSlide', arguments, true);

            // jQuery event
            this.$list.trigger('afterSlide.slider', arguments);
        };

        Slider.prototype.slideNext = function(animationName, animatedHeight) {
            var $next = this.getNextSlide();
            this.slideTo($next, animationName, animatedHeight);
        };

        Slider.prototype.slidePrevious = function(animationName, animatedHeight) {
            var $prev = this.getPreviousSlide();
            this.slideTo($prev, animationName, animatedHeight);
        };

        return Slider;
    })();


    // ================================================
    //            Базовый класс анимации
    // ================================================
    window.SliderPlugin = (function() {
        var SliderPlugin = function(settings) {
            this.opts = $.extend(true, this.getDefaultOpts(), settings);
        };

        // Настройки по умолчанию
        SliderPlugin.prototype.getDefaultOpts = function() {
            return {};
        };

        // Инициализация
        SliderPlugin.prototype.onAttach = function(slider) {

        };

        return SliderPlugin;
    })();


    // ================================================
    //          Плагин мгновенной анимации
    // ================================================
    window.SliderInstantAnimation = (function(parent) {
        // Инициализация плагина
        var InstantAnimation = function(settings) {
            this.opts = $.extend(true, this.getDefaultOpts(), settings);
        };

        var _ = function() {
            this.constructor = InstantAnimation;
        };
        _.prototype = parent.prototype;
        InstantAnimation.prototype = new _;


        // Настройки по умолчанию
        InstantAnimation.prototype.getDefaultOpts = function() {
            return {
                name: 'instant'
            };
        };

        /*
            Реализация метода перехода от одного слайда к другому
         */
        InstantAnimation.prototype.slideTo = function(slider, $toSlide, animatedHeight) {
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

        return InstantAnimation;
    })(SliderPlugin);


    // Обновление высоты слайдера
    $(window).on('load.slider', function() {
        $.each(sliders, function(i, slider) {
            slider.updateListHeight()
        });
    }).on('resize.slider', $.rared(function() {
        $.each(sliders, function(i, slider) {
            slider.opts.onResize.call(slider);

            slider.updateListHeight()
        });
    }, 100));

})(jQuery);
