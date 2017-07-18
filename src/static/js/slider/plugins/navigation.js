(function($) {
    'use strict';

    window.SliderNavigationPlugin = Class(SliderPlugin, function SliderNavigationPlugin(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animateListHeight: true,

            wrapperClass: 'slider-navigation',
            itemClass: 'slider-navigation-item',
            activeItemClass: 'active',

            container: null,
            checkEnabled: function() {
                return this.slider.$slides.length >= 2
            }
        });

        cls.enable = function() {
            this.$wrapper.show();
            superclass.enable.call(this);
        };

        cls.disable = function() {
            this.$wrapper.hide();
            superclass.disable.call(this);
        };

        cls.destroy = function() {
            if (this.$wrapper.length) {
                this.$wrapper.remove();
            }
            superclass.destroy.call(this);
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this.getContainer();
            this.createNavigation();
            this._updateEnabledState();
        };

        /*
            Установка активной кнопки после установки активного слайда
         */
        cls.afterSetCurrentSlide = function($slide) {
            this.activateNavigationItemBySlide($slide);
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        cls.afterSetItemsPerSlide = function() {
            this.updateNavigationItems();
            this.activateNavigationItemBySlide(this.slider.$currentSlide);
            this._updateEnabledState();
        };

        /*
            Получение контейнера для элементов
         */
        cls.getContainer = function() {
            if (typeof this.opts.container === 'string') {
                this.$container = this.slider.$root.find(this.opts.container);
            } else if ($.isFunction(this.opts.container)) {
                this.$container = this.opts.container.call(this);
            } else if (this.opts.container && this.opts.container.jquery) {
                this.$container = this.opts.container;
            }

            if (!this.$container || !this.$container.length) {
                this.$container = this.slider.$root;
            } else if (this.$container.length) {
                this.$container = this.$container.first();
            }
        };

        /*
            Создание кнопок
         */
        cls.createNavigation = function() {
            this.$container.find('.' + this.opts.wrapperClass).remove();
            this.$wrapper = $('<div>').addClass(this.opts.wrapperClass).appendTo(this.$container);

            // событие клика на кнопку
            if (this.opts.animationName) {
                var that = this;
                this.$wrapper.on('click.slider.navigation', '.' + this.opts.itemClass, function() {
                    var $self = $(this);
                    var slideIndex = $self.data('slideIndex') || 0;
                    that.slider.slideTo(
                        that.slider.$slides.eq(slideIndex),
                        that.opts.animationName,
                        that.opts.animateListHeight
                    );
                });
            }

            this.updateNavigationItems();
            this.activateNavigationItemBySlide(this.slider.$currentSlide);
        };

        /*
            Обновление кол-ва кнопок в DOM
         */
        cls.updateNavigationItems = function() {
            // удаление старых точек навигации
            this.$wrapper.find('.' + this.opts.itemClass).remove();

            var that = this;
            $.each(this.slider.$slides, function(index) {
                var $item = $('<a>').addClass(that.opts.itemClass).data('slideIndex', index);
                $item.append($('<span>').text(index + 1));
                that.$wrapper.append($item);
            });
        };

        /*
            Активация соответствующей кнопки по объекту слайда
         */
        cls.activateNavigationItemBySlide = function($slide) {
            var slideIndex = this.slider.$slides.index($slide);
            if (this.$container.length) {
                var $item = this.$container.find('.' + this.opts.itemClass).eq(slideIndex);
                $item.addClass(this.opts.activeItemClass);
                $item.siblings('.' + this.opts.itemClass + '.' + this.opts.activeItemClass)
                    .removeClass(this.opts.activeItemClass);
            }
        };
    });

})(jQuery);
