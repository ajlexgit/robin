(function($) {

    /*
        Основа слайдеров.

        Требует:
            jquery.rared.js

        Может подключать к себе плагины:
            var slider = new Slider($mylist);
            slider.attachPlugin(
                new SliderControlsPlugin({
                    speed: 800
                })
            ).attachPlugin(
                new SliderOtherPlugin()
            );


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

            // настройки
            var defaults = this.getDefaultOpts();
            this.opts = $.extend(true, defaults, settings);

            // сохраняем ссылку на список
            this.$list = this.createList($element);
            this.$list.addClass(this.opts.listClass);

            // оборачиваем список в обертку
            this.$root = this.createRoot($element);
            this.$root.addClass(this.opts.rootClass);
            this.$root.data('slider', this);
            sliders.push(this);

            // сохраняем массив items
            this.$items = this.createItems();
            this.$items.addClass(this.opts.itemClass);

            // создаем слайды
            this.$slides = this.createSlides(this.opts.slideItems);
            this.$slides.addClass(this.opts.slideClass);

            // текущий слайд
            this.$currentSlide = this.getStartSlide();
            this.$currentSlide.css('left', '0');

            this.plugins = [];

            // обновление высоты
            this.updateListHeight();

            // обновление высоты по мере загрузки картинок
            if (this.opts.adaptiveHeight) {
                var $images = this.$currentSlide.find('img');
            } else {
                $images = this.$list.find('img');
            }

            var loadHandle = $.rared(function() {
                that.updateListHeight();
            }, 100);

            $images.one('load', loadHandle);
        };

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
        Slider.prototype.createList = function($element) {
            return $element;
        };

        // Метод, возвращающий ссылку на объект-обертку
        Slider.prototype.createRoot = function($element) {
            $element.wrap('<div>');
            return $element.parent();
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype.createItems = function() {
            return this.$list.find(this.opts.itemSelector);
        };

        // Метод, возвращающий массив ссылок на items
        Slider.prototype.createSlides = function(slideItems) {
            var $slides = $();
            var slide_count = Math.ceil(this.$items.length / slideItems);

            this.$list.empty();
            for (var i=0;i<slide_count;i++) {
                var $slide = $('<div>');
                this.$list.append(
                    $slide.append(
                        this.$items.slice(i * slideItems, (i + 1) * slideItems)
                    )
                );
                $slides.push($slide.get(0));
            }
            return $slides;
        };

        // Метод, возвращающий начальный активный слайд
        Slider.prototype.getStartSlide = function() {
            return this.$slides.first();
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

        // Метод, обновляющий высоту слайдера
        Slider.prototype.updateListHeight = function() {
            if (this.opts.adaptiveHeight) {
                var height = this.$currentSlide.height();
                this.$list.height(height);
            } else {
                var maxHeight = 0;
                $.each(this.$slides, function(i, slide) {
                    var $slide = $(slide);
                    $slide.height('');
                    var height = $slide.height();
                    if (height > maxHeight) {
                        maxHeight = height;
                    }
                });
                this.$list.height(maxHeight);
            }
        };

        // Подключение плагина
        Slider.prototype.attachPlugin = function(plugin) {
            this.plugins.push(plugin);
            plugin.onAttach(this);
            return this;
        };

        // Получение метода плагина по имени
        Slider.prototype.getPluginMethod = function(methodName) {
            var index = this.plugins.length;
            while (index--) {
                var plugin = this.plugins[index];
                if (methodName in plugin) {
                    return plugin[methodName];
                }
            }
        };

        // Переопределяемый метод смены слайда
        Slider.prototype.slide = function($fromSlide, $toSlide) {
            // jQuery event
            this.$list.trigger('beforeSlide.slider', [$fromSlide, $toSlide]);

            var method = this.getPluginMethod('slide');
            if (method) {
                method(this, $fromSlide, $toSlide);
            } else {
                $fromSlide.css({
                    'left': ''
                });
                $toSlide.css({
                    'left': '0'
                });
                this.$currentSlide = $toSlide;
            }

            // jQuery event
            this.$list.trigger('slide.slider', [$fromSlide, $toSlide]);
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
            slider.updateListHeight()
        });
    }).on('resize.slider', $.rared(function() {
        $.each(sliders, function(i, slider) {
            slider.updateListHeight()
        });
    }, 100));

})(jQuery);
