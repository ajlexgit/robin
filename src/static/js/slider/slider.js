(function($) {
    'use strict';

    /*
        Модуль слайдера с подключаемыми плагинами.

        Для упрощения стилизации кода слайдера для случаев, когда JS отключен
        или ещё не загружен, списку можно поставить класс "no-slider".
        Этот класс будет удален, когда слайдер будет готов.

        Требует:
            jquery.utils.js

        Параметры:
            rootClass                       - класс, добавляемый корневому элементу
            listWrapperClass                - класс, добавляемый обертке над списком
            listClass                       - класс, добавляемый списку
            slideClass                      - класс, добавляемый слайду
            itemClass                       - класс, добавляемый элементу списка
            initialActiveClass              - класс начально активного элемента

            itemSelector: str               - селектор элементов слайдера
            itemsPerSlide: number / func    - кол-во элементов на каждый слайд
            loop: bool                      - зацикленный слайдер

            // вариант установки высоты слайдера
            sliderHeight: str
                'current'  - по высоте текущего слайда
                'max'      - по высоте максимального слайда
                'none'     - не задавать высоту

            sliderHeightTransition          - длительность анимации высоты слайдера

        Методы:
            // получение текущего слайда
            getCurrentSlide()

            // установка кол-ва элементов на слайд
            setItemsPerSlide(ips)

            // получение следующего слайда
            getNextSlide()

            // получение предыдущего слайда
            getPreviousSlide()

            // подключение плагинов
            attachPlugins(plugins)

            // перерасчет высоты слайдера
            updateListHeight(animated)

            // переход к слайду $toSlide с анимацией animationName
            slideTo($toSlide, animationName, animateListHeight)

            // переход к следующему слайду
            slideNext(animationName, animateListHeight)

            // переход к предыдущему слайду
            slidePrevious(animationName, animateListHeight)

        События:
            beforeChange                    - перед изменением текущего слайда
            afterChange                     - после изменением текущего слайда

            before_set_ips                  - перед установкой itemsPerSlide
            after_set_ips                   - после установки itemsPerSlide

            beforeSlide                     - перед анимацией перехода к слайду
            afterSlide                      - после анимации перехода к слайду

            startDrag                       - начало перетаскивания слайдов
            stopDrag                        - завершение перетаскивания слайдов

            resize                          - изменение размера окна

        Примечания по событиям:
            1) при инициализации события не вызываются, т.к. их
               обработчики вы ещё не повесили :)

            2) beforeChange / afterChange могут вызываться без beforeSlide.
               Например, при перетаскивании слайда мышкой через несколько слайдов.


        HTML input:
            <div class="slider no-slider">
                <div class="slider-item">...
                <div class="slider-item">
                ...
            </div>

        JS пример:
            Slider('#slider', {
                sliderHeight: Slider.prototype.HEIGHT_MAX,
                loop: false,
                itemsPerSlide: 2
            }).attachPlugins([
                SliderSideAnimation({
                    margin: 20
                }),
                SliderSideShortestAnimation({
                    margin: 20
                }),
                SliderFadeAnimation(),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin({
                    animationName: 'side'
                }),
                SliderDragPlugin({
                    margin: 20
                }),
                SliderAutoscrollPlugin({
                    animationName: 'fade',
                    direction: 'random',
                    interval: 6000
                })
            ]);


        Пример динамического количества элементов в слайде:
            Slider($list, {
                itemsPerSlide: function() {
                    if ($.winWidth() >= 1200)  {
                        return 4
                    } else {
                        return 3
                    }
                }
            }).on('resize', function() {
                // обновление, если значение изменилось
                var itemsPerSlide = this.opts.itemsPerSlide.call(this);
                if (this._itemsPerSlide != itemsPerSlide) {
                    this.setItemsPerSlide(itemsPerSlide);
                }
            });
    */

    /** @namespace window.TweenLite */
    /** @namespace window.TimelineLite */
    var sliders = [];

    window.Slider = Class(EventedObject, function Slider(cls, superclass) {
        // варианты установки высоты слайдера
        cls.HEIGHT_CURRENT = 'current';    // по высоте текущего слайда
        cls.HEIGHT_MAX = 'max';            // по высоте максимального слайда
        cls.HEIGHT_NONE = 'none';          // не устанавливать высоту
        cls.HEIGHT_TYPES = [
            cls.HEIGHT_CURRENT,
            cls.HEIGHT_MAX,
            cls.HEIGHT_NONE
        ];

        cls.defaults = {
            rootClass: 'slider-root',
            listWrapperClass: 'slider-list-wrapper',
            listClass: 'slider-list',
            slideClass: 'slider-slide',
            itemClass: 'slider-item',
            initialActiveClass: 'active',

            itemSelector: '.slider-item',
            itemsPerSlide: 1,
            loop: true,
            sliderHeight: cls.HEIGHT_MAX,
            sliderHeightTransition: 800
        };

        cls.DATA_KEY = 'slider';
        cls.REMOVABLE_CLASS = 'no-slider';

        cls.init = function(list, options) {
            superclass.init.call(this);

            this.$list = $(list).first();
            if (!this.$list.length) {
                return this.raise('list element not found');
            }

            // настройки
            this.opts = $.extend({}, this.defaults, options);

            // плагины
            this._plugins = [];
            this.attachPlugins(SliderInstantAnimation());

            // добавляем класс на список
            this.$list.addClass(this.opts.listClass);

            // создание обертки списка
            this.$listWrapper = this.$list.closest('.' + this.opts.listWrapperClass);
            if (!this.$listWrapper.length) {
                this.$list.wrap('<div>');
                this.$listWrapper = this.$list.parent().addClass(this.opts.listWrapperClass);
            }

            // создание корневого элемента слайдера
            this.$root = this.$listWrapper.closest('.' + this.opts.rootClass);
            if (!this.$root.length) {
                this.$listWrapper.wrap('<div>');
                this.$root = this.$listWrapper.parent().addClass(this.opts.rootClass);
            }

            // сохраняем массив items
            this.$items = this.$list.find(this.opts.itemSelector);
            this.$items.addClass(this.opts.itemClass);

            if (!this.$items.length) {
                return this.raise('there are no items in list');
            }

            // объект анимации
            this._animation = null;

            // текущий элемент
            this.$currentItem = this.$items.filter('.' + this.opts.initialActiveClass).first();
            if (!this.$currentItem.length) {
                this.$currentItem = this.$items.first();
            }

            // создаем слайды
            this.setItemsPerSlide(this.opts.itemsPerSlide);

            // обновление высоты по мере загрузки картинок
            var $images;
            if (this.opts.sliderHeight === this.HEIGHT_CURRENT) {
                $images = this.$currentSlide.find('img');
            } else if (this.opts.sliderHeight === this.HEIGHT_MAX) {
                $images = this.$list.find('img');
            } else if (this.opts.sliderHeight === this.HEIGHT_NONE) {
                $images = $();
            } else {
                return this.raise('unknown sliderHeight');
            }

            if ($images && $images.length) {
                var that = this;
                var loadHandle = $.rared(function() {
                    that.updateListHeight();
                }, 100);

                $images.on('load', loadHandle);
            }

            this.$list.removeClass(this.REMOVABLE_CLASS);
            this.$list.data(this.DATA_KEY, this);
            this.updateListHeight();

            sliders.push(this);
        };

        cls.stopAnimation = function(jumpToEnd) {
            if (!this._animation) return;

            if (window.TweenLite && (this._animation instanceof TweenLite)) {
                this._animation.totalProgress(1);
            } else if (window.TimelineLite && (this._animation instanceof TimelineLite)) {
                this._animation.totalProgress(1);
            } else {
                this._animation.stop(true, jumpToEnd);
            }

            this._animation = null;
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            // Прерывание анимации, если она запущена
            this.stopAnimation(true);
            this.callPluginsMethod('destroy');
            this.$list.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
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
        cls._setCurrentSlide = function($slide) {
            if (!$slide || !$slide.length || (this.$slides.index($slide) < 0)) {
                return false
            }

            if (this.$currentSlide && (this.$currentSlide.get(0) === $slide.get(0))) {
                return false
            }

            this.beforeSetCurrentSlide($slide);
            this.$currentItem = $slide.find('.' + this.opts.itemClass).first();
            this.$currentSlide = $slide;
            this.afterSetCurrentSlide($slide);

            return $slide;
        };

        cls.beforeSetCurrentSlide = function($slide) {
            this.trigger('beforeChange', $slide);
            this.callPluginsMethod('beforeSetCurrentSlide', [$slide]);
        };

        cls.afterSetCurrentSlide = function($slide) {
            this.callPluginsMethod('afterSetCurrentSlide', [$slide], true);
            this.trigger('afterChange', $slide);
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
            if (this._animation) {
                this._animation.stop(true);
                this._animation = null;
            }

            // если функция
            if ($.isFunction(itemsPerSlide)) {
                this._itemsPerSlide = parseInt(itemsPerSlide.call(this));
            } else {
                this._itemsPerSlide = parseInt(itemsPerSlide);
            }
            if (!this._itemsPerSlide) {
                return
            }

            this.beforeSetItemsPerSlide(this._itemsPerSlide);

            // удаляем ранее созданные слайды
            this.$slides = $();

            // сохраняем элементы с их data-значениями
            var $items = this.$items.detach();

            this.$list.find('.' + this.opts.slideClass).remove();

            // создаем слайды
            var slide_count = Math.ceil($items.length / this._itemsPerSlide);
            for (var i = 0; i < slide_count; i++) {
                var $slide = $('<div>');
                this.$list.append(
                    $slide.append(
                        $items.slice(i * this._itemsPerSlide, (i + 1) * this._itemsPerSlide)
                    )
                );
                this.$slides.push($slide.get(0));
            }

            // добавляем слайдам класс
            this.$slides.addClass(this.opts.slideClass);

            // переход к активному слайду
            this.slideTo(this.getCurrentSlide(), 'instant', false);

            this.afterSetItemsPerSlide(this._itemsPerSlide);
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед созданием слайдов.
         */
        cls.beforeSetItemsPerSlide = function(itemsPerSlide) {
            this.trigger('before_set_ips', itemsPerSlide);
            this.callPluginsMethod('beforeSetItemsPerSlide');
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после созданием слайдов.
         */
        cls.afterSetItemsPerSlide = function(itemsPerSlide) {
            this.callPluginsMethod('afterSetItemsPerSlide', null, true);
            this.trigger('after_set_ips', itemsPerSlide);
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
            Подключение плагинов
         */
        cls.attachPlugins = function(plugins) {
            var that = this;
            if ($.isArray(plugins)) {
                plugins.forEach(function(plugin) {
                    if (plugin instanceof window.SliderPlugin) {
                        that._plugins.push(plugin);
                        plugin.onAttach(that);
                    }
                });
            } else if (plugins instanceof window.SliderPlugin) {
                this._plugins.push(plugins);
                plugins.onAttach(this);
            }
            return this;
        };

        /*
            Поиск реализации метода среди плагинов
         */
        cls.getPluginMethod = function(pluginName, methodName) {
            methodName = methodName || 'slideTo';
            var index = this._plugins.length;
            while (index--) {
                var plugin = this._plugins[index];
                if ((methodName in plugin) && (plugin.opts.name === pluginName)) {
                    return $.proxy(plugin[methodName], plugin);
                }
            }

            this.warn('Not found method "' + methodName + '" in plugin "' + pluginName + '"');
        };

        /*
            Вызов метода methodName с агрументами args во всех плагинах,
            в которых этот метод реализован.

            Если reversed=true, обход плагинов будет в обратном порядке
         */
        cls.callPluginsMethod = function(methodName, args, reversed) {
            var plugins = this._plugins.concat();
            if (reversed) {
                plugins.reverse();
            }

            var index = plugins.length;
            while (index--) {
                var plugin = plugins[index];
                if (methodName in plugin) {
                    plugin[methodName].apply(plugin, args);
                }
            }
        };

        // ===============================================
        // ================= update height ===============
        // ===============================================

        /*
            Рассчет высоты слайдера
         */
        cls.calcListHeight = function() {
            if (this.opts.sliderHeight === cls.HEIGHT_CURRENT) {
                return this.$currentSlide.outerHeight();
            } else if (this.opts.sliderHeight === cls.HEIGHT_MAX) {
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
            }
        };

        /*
            Обновление высоты slider.$list в зависимости от высоты слайдов
         */
        cls.updateListHeight = function(doAnimation) {
            // прерываем анимацию высоты, если она идёт
            if (this._list_height_animation) {
                this._list_height_animation.stop(true);
                this._list_height_animation = null;
            }

            var that = this;
            $.animation_frame(function() {
                var final_height = parseInt(that.calcListHeight());
                if (isNaN(final_height)) {
                    return;
                }

                // высота не меняется - выходим
                var current_height = that.$list.height();
                if (current_height === final_height) {
                    return
                }

                that.beforeUpdateListHeight(current_height, final_height);
                if (doAnimation && that.opts.sliderHeightTransition) {
                    // с анимацией
                    that._list_height_animation = that.$list.animate({
                        height: final_height
                    }, {
                        duration: that.opts.sliderHeightTransition,
                        easing: 'easeOutCubic',
                        complete: function() {
                            that.afterUpdateListHeight(current_height, final_height);
                        }
                    });
                } else {
                    // мгновенно
                    that.$list.height(final_height);
                    that.afterUpdateListHeight(current_height, final_height);
                }
            })();
        };

        /*
            Обновление высоты слайдера по условию
         */
        cls.softUpdateListHeight = function(doAnimation) {
            if (this.opts.sliderHeight === cls.HEIGHT_CURRENT) {
                this.updateListHeight(doAnimation);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед обновлением высоты списка.
         */
        cls.beforeUpdateListHeight = function(current, final) {
            this.callPluginsMethod('beforeUpdateListHeight', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после обновления высоты списка.
         */
        cls.afterUpdateListHeight = function(current, final) {
            this.callPluginsMethod('afterUpdateListHeight', arguments, true);
        };


        // ===============================================
        // =============== slide animation ===============
        // ===============================================

        /*
            Метод смены текущего слайда на $toSlide.

            При реализации этого метода в плагинах, НЕОБХОДИМО вызывать
            методы слайдера _beforeSlide и _afterSlide:
                this.slider._beforeSlide($toSlide);
                ....
                this.slider._afterSlide($toSlide);

            Объект анимации (если он есть) НЕОБХОДИМО сохранить в переменной
            this.slider._animation
         */
        cls.slideTo = function($toSlide, animationName, animateListHeight) {
            if (!$toSlide || !$toSlide.length || (this.$slides.index($toSlide) < 0)) {
                return
            }

            // скролл к уже активному слайду
            if (this.$currentSlide && (this.$currentSlide.get(0) === $toSlide.get(0))) {
                return
            }

            animationName = animationName || 'instant';
            var method = this.getPluginMethod(animationName);
            if (method) {
                method($toSlide, animateListHeight);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед анимацией изменения текущего слайда (любым из плагинов).
         */
        cls._beforeSlide = function($toSlide) {
            this.trigger('beforeSlide', $toSlide);
            this.callPluginsMethod('beforeSlide', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            после завершения анимации изменения текущего слайда (любым из плагинов).
         */
        cls._afterSlide = function($toSlide) {
            this.callPluginsMethod('afterSlide', arguments, true);
            this.trigger('afterSlide', $toSlide);
        };

        cls.slideNext = function(animationName, animateListHeight) {
            var $slide = this.getNextSlide();
            this.slideTo($slide, animationName, animateListHeight);
        };

        cls.slidePrevious = function(animationName, animateListHeight) {
            var $slide = this.getPreviousSlide();
            this.slideTo($slide, animationName, animateListHeight);
        };

        cls.slideRandom = function(animationName, animateListHeight) {
            var slides_count = this.$slides.length;
            var random_index = Math.floor(Math.random() * (slides_count - 1));
            var current_index = this.$slides.index(this.$currentSlide);
            var final_index = (random_index < current_index) ? random_index : random_index + 1;

            var $slide = this.$slides.eq(final_index);
            this.slideTo($slide, animationName, animateListHeight);
        };
    });


    // ================================================
    //            Базовый класс плагина
    // ================================================
    window.SliderPlugin = Class(Object, function SliderPlugin(cls, superclass) {
        cls.defaults = {
            checkEnabled: $.noop
        };

        cls.init = function(settings) {
            this.opts = $.extend(true, {}, this.defaults, settings);
        };

        cls.destroy = function() {
            var plugin_index = this.slider._plugins.indexOf(this);
            if (plugin_index >= 0) {
                this.slider._plugins.splice(plugin_index, 1);
            }
        };

        // Инициализация
        cls.onAttach = function(slider) {
            this.slider = slider;
        };

        // Событие изменения размера окна
        cls.onResize = function() {

        };

        /*
            Проверка включенности и включение / выключение
         */
        cls._updateEnabledState = function() {
            var status = this.opts.checkEnabled.call(this) !== false;
            if (this.enabled === status) return;

            this.enabled = status;
            if (this.enabled) {
                this.enable();
            } else {
                this.disable();
            }
        };

        // Включение
        cls.enable = function() {
            this.enabled = true;
        };

        // Выключение
        cls.disable = function() {
            this.enabled = false;
        };
    });


    // ================================================
    //          Плагин мгновенной анимации
    // ================================================
    window.SliderInstantAnimation = Class(window.SliderPlugin, function SliderInstantAnimation(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            name: 'instant'
        });

        /*
            Реализация метода перехода от одного слайда к другому
         */
        cls.slideTo = function($toSlide, animateListHeight) {
            if (this.slider._animation) {
                return
            }

            this.slider._beforeSlide($toSlide);
            this.slider.$slides.css({
                transform: ''
            });
            $toSlide.css({
                transform: 'none'
            });
            this.slider._setCurrentSlide($toSlide);
            this.slider._afterSlide($toSlide);
            this.slider.softUpdateListHeight(animateListHeight);
        };
    });

    // Обновление высоты слайдера
    $(window).on('load.slider', function() {
        $.each(sliders, function(i, slider) {
            slider.updateListHeight()
        });
    }).on('resize.slider', $.rared(function() {
        $.each(sliders, function(i, slider) {
            slider.trigger('resize');
            slider.callPluginsMethod('onResize');
            slider.updateListHeight();
        });
    }, 100));

})(jQuery);
