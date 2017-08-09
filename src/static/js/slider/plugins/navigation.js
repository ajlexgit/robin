(function($) {
    'use strict';

    window.SliderNavigationPlugin = Class(SliderPlugin, function SliderNavigationPlugin(cls, superclass) {
        cls.PLUGIN_NAME = 'navigation';

        cls.defaults = $.extend({}, superclass.defaults, {
            animationName: '',
            animationOptions: {
                animateListHeight: true
            },

            wrapperClass: 'slider-navigation',
            itemClass: 'slider-navigation-item',
            activeItemClass: 'active',

            container: null,
            checkEnabled: function() {
                return this.slider.$slides.length >= 2
            }
        });

        cls.init = function(settings) {
            superclass.init.call(this, settings);
            this._createDOM();
        };

        cls.enable = function() {
            this.$wrapper.css('display', '');
            superclass.enable.call(this);
        };

        cls.disable = function() {
            this.$wrapper.hide();
            superclass.disable.call(this);
        };

        cls.destroy = function() {
            this.$wrapper.remove();
            superclass.destroy.call(this);
        };

        /*
            Создание кнопок при подключении плагина
         */
        cls.onAttach = function(slider) {
            superclass.onAttach.call(this, slider);
            this._attachDOM();
            this._attachEvents();
            this.updateNavigationItems();
            this.activateNavigationItem();
            this._updateEnabledState();
        };

        /*
            Обновление кнопок при изменении кол-ва элементов в слайде
         */
        cls.onChangeItemsPerSlide = function() {
            this.updateNavigationItems();
            this.activateNavigationItem();
            this._updateEnabledState();
        };

        /*
            Установка активной кнопки после установки активного слайда
         */
        cls.onChangeCurrentSlide = function() {
            this.activateNavigationItem();
        };

        /*
            Создание DOM-элементов стрелок
         */
        cls._createDOM = function() {
            this.$wrapper = $('<div>').addClass(this.opts.wrapperClass);
        };

        /*
            Навешивание событий
         */
        cls._attachEvents = function() {
            var that = this;
            if (this.opts.animationName) {
                this.$wrapper.off('.navigation');
                this.$wrapper.on('click.slider.navigation', '.' + this.opts.itemClass, function() {
                    var slideIndex = $(this).data('slideIndex') || 0;
                    that.slider.slideTo(
                        that.slider.$slides.eq(slideIndex),
                        that.opts.animationName,
                        that.opts.animationOptions
                    );
                });
            }
        };

        /*
            Добавление кнопок в DOM-дерево
         */
        cls._attachDOM = function() {
            this.getContainer().append(this.$wrapper);
        };

        /*
            Получение контейнера для элементов
         */
        cls.getContainer = function() {
            if (typeof this.opts.container === 'string') {
                var $container = this.slider.$root.find(this.opts.container);
            } else if ($.isFunction(this.opts.container)) {
                $container = this.opts.container.call(this);
            } else if (this.opts.container && this.opts.container.jquery) {
                $container = this.opts.container;
            }

            if (!$container || !$container.length) {
                $container = this.slider.$root;
            } else if ($container.length) {
                $container = $container.first();
            }

            return $container;
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
            Активация текущей кнопки
         */
        cls.activateNavigationItem = function() {
            var $slide = this.slider.$currentSlide;
            var slideIndex = this.slider.$slides.index($slide);
            var $item = this.$wrapper.find('.' + this.opts.itemClass).eq(slideIndex);

            $item.addClass(this.opts.activeItemClass);
            $item.siblings('.' + this.opts.itemClass).removeClass(this.opts.activeItemClass);
        };
    });

})(jQuery);
