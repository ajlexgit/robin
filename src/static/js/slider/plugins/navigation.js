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
                wrapperDisabledClass: 'slider-navigation-disabled',
                itemClass: 'slider-navigation-item',
                activeItemClass: 'active',

                container: null,
                dragOneSlide: false
            };
        };

        /*
            Создание кнопок при подключении плагина
         */
        NavigationPlugin.prototype.onAttach = function(slider) {
            parent.prototype.onAttach.call(this, slider);

            this.createNavigation(slider);
            this.checkEnabled(slider);
        };

        /*
            Установка активной кнопки после установки активного слайда
         */
        NavigationPlugin.prototype.afterSetCurrentSlide = function(slider, $slide) {
            this.activateNavigationItemBySlide(slider, $slide);
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        NavigationPlugin.prototype.afterSetSlideItems = function(slider) {
            this.createNavigation(slider);
            this.checkEnabled(slider);
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
                var $container = $.findFirstElement(this.opts.container, slider);
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
            this.$wrapper = $('<div/>').addClass(this.opts.wrapperClass).appendTo(this.$container);

            for (var i = 0; i < slider.$slides.length; i++) {
                var $item = $('<a>').addClass(this.opts.itemClass)
                    .data('slideIndex', i)
                    .text(i + 1);
                this.$wrapper.append($item);
            }

            var that = this;
            this.$wrapper.on('click.slider.navigation', '.' + this.opts.itemClass, function() {
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

        /*
            Деактивация навигации на одном слайде
         */
        NavigationPlugin.prototype.checkEnabled = function(slider) {
            if (!this.opts.dragOneSlide && (slider.$slides.length < 2)) {
                this.$wrapper.addClass(this.opts.wrapperDisabledClass);
            } else {
                this.$wrapper.removeClass(this.opts.wrapperDisabledClass);
            }
        };

        return NavigationPlugin;
    })(SliderPlugin);

})(jQuery);
