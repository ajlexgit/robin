(function($) {

    window.SliderNavigationPlugin = (function(parent) {
        // Инициализация плагина
        var NavigationPlugin = function(settings) {
            parent.call(this, settings);

            if (!this.opts.animationName) {
                console.error('Navigation plugin must set animationName');
            }
        };

        var _ = function() {
            this.constructor = NavigationPlugin;
        };
        _.prototype = parent.prototype;
        NavigationPlugin.prototype = new _;


        // Настройки по умолчанию
        NavigationPlugin.prototype.getDefaultOpts = function() {
            return {
                animationName: '',
                animatedHeight: true,

                wrapperClass: 'slider-navigation',
                itemClass: 'slider-navigation-item',
                activeItemClass: 'active',

                container: null
            };
        };

        /*
            Создание кнопок при подключении плагина
         */
        NavigationPlugin.prototype.onAttach = function(slider) {
            parent.prototype.onAttach.call(this, slider);

            this.createNavigation(slider);
        };

        /*
            Установка активной кнопки после укстановки активного слайда
         */
        NavigationPlugin.prototype.afterSetCurrentSlide = function(slider, $slide) {
            this.activateNavigationItemBySlide(slider, $slide);
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        NavigationPlugin.prototype.afterSetSlideItems = function(slider) {
            this.createNavigation(slider);
        };


        /*
            Создание кнопок
         */
        NavigationPlugin.prototype.createNavigation = function(slider) {
            this.$container = this.getContainer(slider);
            if (this.$container.length) {
                this.$container = this.$container.first();
                this.createNavigationItems(slider);
                this.activateNavigationItemBySlide(slider, slider.$currentSlide);
            } else {
                this.$container = null;
            }
        };

        /*
            Возвращает контейнер, в который будут добавлены кнопки
         */
        NavigationPlugin.prototype.getContainer = function(slider) {
            if (this.opts.container) {
                var $container = $(this.opts.container);
            } else {
                $container = slider.$root
            }
            return $container;
        };

        /*
            Добавление кнопок в DOM
         */
        NavigationPlugin.prototype.createNavigationItems = function(slider) {
            this.$container.find('.' + this.opts.wrapperClass).remove();
            var $wrapper = $('<div/>').addClass(this.opts.wrapperClass);
            this.$container.append($wrapper);

            for (var i = 0; i < slider.$slides.length; i++) {
                var $item = $('<a>').addClass(this.opts.itemClass)
                    .data('slideIndex', i)
                    .text(i + 1);
                $wrapper.append($item);
            }

            var that = this;
            $wrapper.on('click.slider.navigation', '.' + this.opts.itemClass, function() {
                var $self = $(this);
                var slideIndex = $self.data('slideIndex') || 0;
                slider.slideTo(slider.$slides.eq(slideIndex), that.opts.animationName, that.opts.animatedHeight);
            });
        };

        /*
            Активация соответствующей кнопки по объекту слайда
         */
        NavigationPlugin.prototype.activateNavigationItemBySlide = function(slider, $slide) {
            var slideIndex = slider.$slides.index($slide);
            if (this.$container.length) {
                var $item = this.$container.find('.' + this.opts.itemClass).eq(slideIndex);
                $item.addClass(this.opts.activeItemClass);
                $item.siblings('.' + this.opts.itemClass + '.' + this.opts.activeItemClass)
                    .removeClass(this.opts.activeItemClass);
            }
        };

        return NavigationPlugin;
    })(SliderPlugin);

})(jQuery);
