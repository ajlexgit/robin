(function($) {

    /*
        Основа слайдеров.

        Требует:
            jquery.rared.js, jquery.animation.js

        HTML input:
            <div class="slider">
                <img>
                <img>
                ...
            </div>

        JS пример:
            var slider = new Slider('#slider', {
                loop: true,
                adaptiveHeight: true,
                adaptiveHeightTransition: 800,
                slideItems: 1
            }).attachPlugin(
                new SliderSideAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                })
            ).attachPlugin(
                new SliderSideLoopAnimation({
                    speed: 800,
                    slideMarginPercent: 5
                })
            ).attachPlugin(
                new SliderFadeAnimation()
            ).attachPlugin(
                new SliderControlsPlugin({
                    animationName: 'side-loop'
                })
            ).attachPlugin(
                new SliderNavigationPlugin({
                    animationName: 'side'
                })
            ).attachPlugin(
                new SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 3000
                })
            );
    */

    var sliders = [];

    window.Slider = (function() {
        var Slider = function(element, settings) {
            var $element = $(element).first();
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
                that.updateListHeight(that.opts.initialAnimatedHeight);
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

                itemSelector: 'img',
                slideItems: 1,
                loop: true,
                adaptiveHeight: true,
                adaptiveHeightTransition: 800
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
            Подключение плагина.

            Пример:
                var slider = new Slider($mylist, {
                    adaptiveHeight: false
                }).attachPlugin(
                    new ControlsPlugin()
                ).attachPlugin(
                    new SideAnimation()
                );
         */
        Slider.prototype.attachPlugin = function(plugin) {
            this._plugins.push(plugin);
            plugin.onAttach(this);
            return this;
        };

        /*
            Поиск реализации метода анимации среди плагинов
         */
        Slider.prototype.getAnimationMethod = function(animationName) {
            var index = this._plugins.length;
            while (index--) {
                var plugin = this._plugins[index];
                if (('slideTo' in plugin) && (plugin.opts.name == animationName)) {
                    return $.proxy(plugin.slideTo, plugin);
                }
            }
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

        // Активация слайда
        Slider.prototype._setCurrentSlide = function($slide) {
            this.$currentSlide = $slide;
        };

        // Метод, возвращающий следующий слайд
        Slider.prototype.getNextSlide = function($fromSlide) {
            if (!$fromSlide || !$fromSlide.length) {
                $fromSlide = this.$currentSlide;
            }

            var index = this.$slides.index($fromSlide);
            if (++index < this.$slides.length) {
                return this.$slides.eq(index);
            }

            if (this.opts.loop) {
                return this.$slides.eq(0);
            }
        };

        // Метод, возвращающий предыдущий слайд
        Slider.prototype.getPreviousSlide = function($fromSlide) {
            if (!$fromSlide || !$fromSlide.length) {
                $fromSlide = this.$currentSlide;
            }

            var index = this.$slides.index($fromSlide);
            if (--index >= 0) {
                return this.$slides.eq(index);
            }

            if (this.opts.loop) {
                return this.$slides.eq(this.$slides.length - 1);
            }
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
            this.callPluginsMethod('beforeSetSlideItems');

            // jQuery event
            this.$list.trigger('beforeSetSlideItems.slider');
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после созданием слайдов.
         */
        Slider.prototype.afterSetSlideItems = function() {
            // jQuery event
            this.$list.trigger('afterSetSlideItems.slider');

            this.callPluginsMethod('afterSetSlideItems', null, true);
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

            if (this.opts.adaptiveHeight) {
                final_height = this.$currentSlide.outerHeight();
            } else {
                $.each(this.$slides, function(i, slide) {
                    var $slide = $(slide);
                    $slide.height('');
                    var height = $slide.outerHeight();
                    if (height > final_height) {
                        final_height = height;
                    }
                });
            }

            if (current_height != final_height) {
                if (this._adaptive_animation) {
                    this._adaptive_animation.stop();
                }

                this.beforeUpdateListHeight(current_height, final_height, animatedHeight);
                if (animatedHeight && this.opts.adaptiveHeightTransition) {
                    var that = this;
                    this._adaptive_animation = $.animate({
                        duration: this.opts.adaptiveHeightTransition,
                        delay: 60,
                        easing: 'easeOutCubic',
                        init: function() {
                            this.initial = that.$list.outerHeight();
                            this.diff = final_height - this.initial;
                        },
                        step: function(eProgress) {
                            var height = this.initial + (this.diff * eProgress);
                            $.animation_frame(function() {
                                that.$list.outerHeight(height);
                            }, that.$list.get(0))();
                        }
                    })
                } else {
                    this.$list.outerHeight(final_height);
                }

                this.afterUpdateListHeight(current_height, final_height, animatedHeight);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед обновлением высоты списка.
         */
        Slider.prototype.beforeUpdateListHeight = function(current, final, animatedHeight) {
            this.callPluginsMethod('beforeUpdateListHeight', arguments);

            // jQuery event
            this.$list.trigger('beforeUpdateListHeight.slider', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после обновления высоты списка.
         */
        Slider.prototype.afterUpdateListHeight = function(current, final, animatedHeight) {
            // jQuery event
            this.$list.trigger('afterUpdateListHeight.slider', arguments);

            this.callPluginsMethod('afterUpdateListHeight', arguments, true);
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
            if (!$toSlide.length || (this.$slides.index($toSlide) < 0)) {
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
            } else {
                console.error('Not found animation method named "' + animationName + '"');
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед переходом к слайду.
         */
        Slider.prototype.beforeSlide = function($toSlide) {
            this._animated = true;

            this.callPluginsMethod('beforeSlide', arguments);

            // jQuery event
            this.$list.trigger('beforeSlide.slider', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после перехода к слайду.
         */
        Slider.prototype.afterSlide = function($toSlide) {
            // jQuery event
            this.$list.trigger('afterSlide.slider', arguments);

            this.callPluginsMethod('afterSlide', arguments, true);

            this._animated = false;
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
            slider._setCurrentSlide($toSlide);
            slider.updateListHeight(animatedHeight);

            slider.afterSlide($toSlide);
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
            slider.updateListHeight()
        });
    }, 100));

})(jQuery);
