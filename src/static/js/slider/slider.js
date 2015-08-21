(function($) {

    /*
        Основа слайдеров.

        Требует:
            jquery.rared.js

        HTML input:
            <div class="slider">
                <img>
                <img>
                ...
            </div>

        JS пример:
            var slider = new Slider($elem, {
                slideItems: 2
            }).attachPlugin(
                new SliderControlsPlugin()
            ).attachPlugin(
                new SliderNavigationPlugin()
            ).attachPlugin(
                new SliderSideAnimation({
                    speed: 1000
                })
            );
    */

    var sliders = [];

    window.Slider = (function() {
        var Slider = function($element, settings) {
            if (!$element || !$element.length) {
                return
            }

            var that = this;

            this._plugins = [];
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
            this.slideNowTo($startSlide, true);

            // обновление высоты по мере загрузки картинок
            if (this.opts.adaptiveHeight) {
                var $images = this.$currentSlide.find('img');
            } else {
                $images = this.$list.find('img');
            }

            var loadHandle = $.rared(function() {
                that.updateListHeight(true);
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

                itemSelector: 'img',
                slideItems: 1,
                loop: true,
                adaptiveHeight: true
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
            Поиск первой реализации метода methodName среди плагинов,
            начиная с последнего подключенного
         */
        Slider.prototype.getFirstPluginMethod = function(methodName) {
            var index = this._plugins.length;
            while (index--) {
                var plugin = this._plugins[index];
                if (methodName in plugin) {
                    return $.proxy(plugin[methodName], plugin);
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
            this.slideNowTo($startSlide);

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
        Slider.prototype.updateListHeight = function(forced) {
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
                this.beforeUpdateListHeight(forced, current_height, final_height);
                this.$list.outerHeight(final_height);

                // отдельным кадром анимации, чтобы избежать схлопывания изменений стилей
                var that = this;
                setTimeout(function() {
                    that.afterUpdateListHeight(forced, current_height, final_height);
                }, 1000 / 60);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед обновлением высоты списка.
         */
        Slider.prototype.beforeUpdateListHeight = function(forced, current, final) {
            this.callPluginsMethod('beforeUpdateListHeight', arguments);

            // jQuery event
            this.$list.trigger('beforeUpdateListHeight.slider', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после обновления высоты списка.
         */
        Slider.prototype.afterUpdateListHeight = function(forced, current, final) {
            // jQuery event
            this.$list.trigger('afterUpdateListHeight.slider', arguments);

            this.callPluginsMethod('afterUpdateListHeight', arguments, true);
        };


        // ===============================================
        // =============== slide animation ===============
        // ===============================================

        /*
            Переопределяемый метод смены текущего слайда на $toSlide БЕЗ АНИМАЦИИ.

            Плагины могут переопределить этот метод. Будет использован метод
            плагина, подключенного последним.

            В реализации этого метода НЕОБХОДИМО вызывать методы слайдера
            beforeSlide и afterSlide:
                slider.beforeSlide($toSlide, true);
                ....
                slider.afterSlide($toSlide, true);
         */
        Slider.prototype.slideNowTo = function($toSlide, forceListHeight) {
            if (!$toSlide.length || (this.$slides.index($toSlide) < 0)) {
                return
            }

            // скролл к уже активному слайду
            if (this.$currentSlide.get(0) === $toSlide.get(0)) {
                return
            }

            var final_args = this._argsWithThis(arguments);
            var method = this.getFirstPluginMethod('slideNowTo');
            if (method) {
                method.apply(null, final_args);
            } else {
                // поведение по умолчанию
                this.beforeSlide($toSlide, true);

                this.$slides.css({
                    left: ''
                });
                $toSlide.css({
                    left: '0'
                });
                this._setCurrentSlide($toSlide);

                this.updateListHeight(forceListHeight);

                this.afterSlide($toSlide, true);
            }
        };

        /*
            Переопределяемый метод смены текущего слайда на $toSlide.

            Плагины могут переопределить этот метод. Будет использован метод
            плагина, подключенного последним.

            В реализации этого метода НЕОБХОДИМО вызывать методы слайдера
            beforeSlide и afterSlide:
                slider.beforeSlide($toSlide);
                ....
                slider.afterSlide($toSlide);
         */
        Slider.prototype.slideTo = function($toSlide, forceListHeight) {
            if (!$toSlide.length || (this.$slides.index($toSlide) < 0)) {
                return
            }

            // скролл к уже активному слайду
            if (this.$currentSlide.get(0) === $toSlide.get(0)) {
                return
            }

            var final_args = this._argsWithThis(arguments);
            var method = this.getFirstPluginMethod('slideTo');
            if (method) {
                method.apply(null, final_args);
            } else {
                // поведение по умолчанию
                this.beforeSlide($toSlide);

                this.$slides.css({
                    left: ''
                });
                $toSlide.css({
                    left: '0'
                });
                this._setCurrentSlide($toSlide);

                this.updateListHeight(forceListHeight);

                this.afterSlide($toSlide);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед переходом к слайду.
         */
        Slider.prototype.beforeSlide = function($toSlide, instantly) {
            this.callPluginsMethod('beforeSlide', arguments);

            // jQuery event
            this.$list.trigger('beforeSlide.slider', arguments);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после перехода к слайду.
         */
        Slider.prototype.afterSlide = function($toSlide, instantly) {
            // jQuery event
            this.$list.trigger('afterSlide.slider', arguments);

            this.callPluginsMethod('afterSlide', arguments, true);
        };

        return Slider;
    })();


    window.SliderPlugin = (function() {
        var SliderPlugin = function(settings) {

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


    // Обновление высоты слайдера
    $(window).on('load.slider', function() {
        $.each(sliders, function(i, slider) {
            slider.updateListHeight(true)
        });
    }).on('resize.slider', $.rared(function() {
        $.each(sliders, function(i, slider) {
            slider.updateListHeight(true)
        });
    }, 100));

})(jQuery);
