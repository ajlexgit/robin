(function($) {
    'use strict';

    window.SliderNavigationPlugin = Class(SliderPlugin, function SliderNavigationPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animatedHeight: true,

            wrapperClass: 'slider-navigation',
            wrapperDisabledClass: 'slider-navigation-disabled',
            itemClass: 'slider-navigation-item',
            activeItemClass: 'active',

            container: null,
            dragOneSlide: false
        });


        cls.init = function(settings) {
            superclass.init.call(this, settings);
            if (!this.opts.animationName) {
                return this.raise('animationName required');
            }
        };

        cls.destroy = function() {
            if (this.$wrapper) {
                this.$wrapper.remove();
                this.$wrapper = null;
            }
            superclass.destroy.call(this);
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this.createNavigation(slider);
            this.checkEnabled(slider);
        };

        /*
            Установка активной кнопки после установки активного слайда
         */
        cls.afterSetCurrentSlide = function(slider, $slide) {
            this.activateNavigationItemBySlide(slider, $slide);
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        cls.afterSetItemsPerSlide = function(slider) {
            this.createNavigation(slider);
            this.checkEnabled(slider);
        };

        /*
            Создание кнопок
         */
        cls.createNavigation = function(slider) {
            if (this.opts.container) {
                this.$container = slider.$root.find(this.opts.container).first();
            } else {
                this.$container = slider.$root
            }

            if (this.$container.length) {
                this.createNavigationItems(slider);
                this.activateNavigationItemBySlide(slider, slider.$currentSlide);
            } else {
                this.$container = null;
            }
        };

        /*
            Добавление кнопок в DOM
         */
        cls.createNavigationItems = function(slider) {
            // удаление старых точек навигации
            this.$container.find('.' + this.opts.wrapperClass).remove();
            this.$wrapper = $('<div/>').addClass(this.opts.wrapperClass).appendTo(this.$container);

            for (var i = 0; i < slider.$slides.length; i++) {
                var $item = $('<a>').addClass(this.opts.itemClass).data('slideIndex', i);
                $item.append($('<span>').text(i+1));
                this.$wrapper.append($item);
            }

            var that = this;
            this.$wrapper.on(touchClick + '.slider.navigation', '.' + this.opts.itemClass, function() {
                var $self = $(this);
                var slideIndex = $self.data('slideIndex') || 0;
                slider.slideTo(
                    slider.$slides.eq(slideIndex),
                    that.opts.animationName,
                    that.opts.animatedHeight
                );
            });
        };

        /*
            Активация соответствующей кнопки по объекту слайда
         */
        cls.activateNavigationItemBySlide = function(slider, $slide) {
            var slideIndex = slider.$slides.index($slide);
            if (this.$container.length) {
                var $item = this.$container.find('.' + this.opts.itemClass).eq(slideIndex);
                $item.addClass(this.opts.activeItemClass);
                $item.siblings('.' + this.opts.itemClass + '.' + this.opts.activeItemClass)
                    .removeClass(this.opts.activeItemClass);
            }
        };

        /*
            Деактивация навигации когда в слайдере всего один слайд
         */
        cls.checkEnabled = function(slider) {
            if (!this.opts.dragOneSlide && (slider.$slides.length < 2)) {
                this.$wrapper.addClass(this.opts.wrapperDisabledClass);
            } else {
                this.$wrapper.removeClass(this.opts.wrapperDisabledClass);
            }
        };
    });

})(jQuery);
