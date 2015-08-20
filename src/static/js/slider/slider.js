(function($) {

    /*
        Основа слайдеров.

        Требует:
            jquery.rared.js

        HTML input:
            <div>
                <img>
                ...
            </div>

        HTML output:
            <div role="root">
                <ul role="list">
                    <li role="slide">
                        <img role="item">
                        <img role="item">
                        ...
                    </li>
                    ...
                </ul>
            </div>
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

            // оборачиваем список в обертку
            this.$root = this._createRoot($element);
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
            this._setCurrentSlide($startSlide, true);

            // обновление высоты
            this.updateListHeight(true);

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
        // ============== system methods =================
        // ===============================================

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
            Вызом метода methodName с агрументами args во всех плагинах,
            в которых этот метод реализован.
            Если reversed=true, обход плагинов будет в обратном порядке
            (от поключенных первыми)
         */
        Slider.prototype.callPluginsMethod = function(methodName, args, reversed) {
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
        // =========== initialization methods ============
        // ===============================================

        // Метод, возвращающий объект настроек по умолчанию
        Slider.prototype.getDefaultOpts = function() {
            return {
                rootClass: 'slider-root',
                listClass: 'slider-list',
                slideClass: 'slider-slide',
                itemClass: 'slider-item',

                itemSelector: 'img',
                slideItems: 2,
                loop: true,
                adaptiveHeight: true
            };
        };

        // Метод, возвращающий ссылку на объект-список
        Slider.prototype._createList = function($element) {
            return $element;
        };

        // Метод, возвращающий ссылку на объект-обертку
        Slider.prototype._createRoot = function($element) {
            $element.wrap('<div>');
            return $element.parent();
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype._createItems = function() {
            return this.$list.find(this.opts.itemSelector);
        };

        // ===============================================
        // =============== slides methods ================
        // ===============================================

        // Метод, возвращающий начально активный слайд
        Slider.prototype._getStartSlide = function() {
            return this.$slides.first();
        };

        // Активация слайда
        Slider.prototype._setCurrentSlide = function($slide, instantly) {
            this.$currentSlide = $slide;

            if (instantly) {
                $slide.css({
                    left: '0'
                });
            }
        };

        // Метод, возвращающий следующий слайд
        Slider.prototype.getNextSlide = function($slide) {
            var index = this.$slides.index($slide);
            if (++index < this.$slides.length) {
                return this.$slides.eq(index);
            }

            if (this.opts.loop) {
                return this.$slides.eq(0);
            }
        };

        // Метод, возвращающий предыдущий слайд
        Slider.prototype.getPreviousSlide = function($slide) {
            var index = this.$slides.index($slide);
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

            // активация текущего слайда
            var $startSlide = $current_item.closest('.' + this.opts.slideClass);
            this._setCurrentSlide($startSlide, true);

            this.afterSetSlideItems();

            // обновление высоты
            this.updateListHeight(true);
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед созданием слайдов.
         */
        Slider.prototype.beforeSetSlideItems = function() {
            this.callPluginsMethod('beforeSetSlideItems', [this]);

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

            this.callPluginsMethod('afterSetSlideItems', [this], true);
        };


        // ===============================================
        // ================= update height ===============
        // ===============================================

        /*
            Обновление высоты slider.$list в зависимости от высоты слайдов
            и настройки adaptiveHeight
         */
        Slider.prototype.updateListHeight = function(instantly) {
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
                this.beforeUpdateListHeight(instantly, current_height, final_height);
                this.$list.outerHeight(final_height);

                // отдельным кадром анимации, чтобы избежать схлопывания изменений стилей
                var that = this;
                setTimeout(function() {
                    that.afterUpdateListHeight(instantly, current_height, final_height);
                }, 1000 / 60);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед обновлением высоты списка.
         */
        Slider.prototype.beforeUpdateListHeight = function(instantly, current, final) {
            this.callPluginsMethod('beforeUpdateListHeight', [this, instantly, current, final]);

            // jQuery event
            this.$list.trigger('beforeUpdateListHeight.slider', [instantly, current, final]);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после обновления высоты списка.
         */
        Slider.prototype.afterUpdateListHeight = function(instantly, current, final) {
            // jQuery event
            this.$list.trigger('afterUpdateListHeight.slider', [instantly, current, final]);

            this.callPluginsMethod('afterUpdateListHeight', [this, instantly, current, final], true);
        };

        // ===============================================
        // =============== slide animation ===============
        // ===============================================

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
        Slider.prototype.slideTo = function($toSlide) {
            if (!$toSlide.length || (this.$slides.index($toSlide) < 0)) {
                return
            }

            var method = this.getFirstPluginMethod('slideTo');
            if (method) {
                method(this, $toSlide);
            } else {
                // поведение по умолчанию
                this.beforeSlide($toSlide);

                this.$slides.css({
                    left: ''
                });

                this._setCurrentSlide($toSlide, true);

                if (this.opts.adaptiveHeight) {
                    this.updateListHeight()
                }

                this.afterSlide($toSlide);
            }
        };

        /*
            Метод, вызываемый в каждом плагине (от последнего к первому)
            перед переходом к слайду.
         */
        Slider.prototype.beforeSlide = function($toSlide) {
            this.callPluginsMethod('beforeSlide', [this, $toSlide]);

            // jQuery event
            this.$list.trigger('beforeSlide.slider', [$toSlide]);
        };

        /*
            Метод, вызываемый в каждом плагине (от первого к последнему)
            после перехода к слайду.
         */
        Slider.prototype.afterSlide = function($toSlide) {
            // jQuery event
            this.$list.trigger('afterSlide.slider', [$toSlide]);

            this.callPluginsMethod('afterSlide', [this, $toSlide], true);
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
