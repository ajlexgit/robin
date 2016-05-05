(function($) {
    'use strict';

    /*
        Класс, отвечающий за показ/скрытие меню при нажатии кнопки.

        Требует:
            jquery.utils.js

        Параметры:
            menuSelector        - селектор элемента меню
            menuActiveClass     - класс меню, когда оно активно
            buttonSelector      - селектор кнопки, активирующей меню
            buttonActiveClass   - класс кнопки, когда меню активно

            fullHeight          - должно ли меню быть на всю высоту

        События:
            // Перед показом мобильного меню
            before_show

            // Перед скрытием мобильного меню
            before_hide

            // Изменение размера окна
            resize
    */

    var menus = [];

    var Menu = Class(EventedObject, function Menu(cls, superclass) {
        cls.init = function(options) {
            superclass.init.call(this);

            this.opts = $.extend({
                menuSelector: '#mobile-menu',
                menuActiveClass: 'active',
                buttonSelector: '#mobile-menu-button',
                buttonActiveClass: 'active',

                fullHeight: false
            }, options);

            // элемент меню
            this.$menu = $(this.opts.menuSelector).first();
            if (!this.$menu.length) {
                return this.raise('menu element not found');
            }

            var that = this;

            // клик на кнопку
            $(document).off('.menu').on('click.menu', this.opts.buttonSelector, function() {
                return that.onClick($(this));
            });

            menus.push(this);
        };

        /*
            Обработчик нажатия кнопки
         */
        cls.onClick = function($button) {
            var currently_active = $button.hasClass(this.opts.buttonActiveClass);
            if (currently_active) {
                this.hide()
            } else {
                this.show()
            }

            return false;
        };

        /*
            Показ меню
         */
        cls.show = function() {
            if (this.trigger('before_show') === false) {
                return false;
            }

            if (this.opts.fullHeight) {
                // на всю высоту окна
                this.$menu.height('auto');
                var default_height = this.$menu.outerHeight();
                this.$menu.outerHeight(Math.max(default_height, $.winHeight()));
            }

            $(this.opts.buttonSelector).addClass(this.opts.buttonActiveClass);
            this.$menu.addClass(this.opts.menuActiveClass);
        };

        /*
            Скрытие меню
         */
        cls.hide = function() {
            if (this.trigger('before_hide') === false) {
                return false;
            }

            $(this.opts.buttonSelector).removeClass(this.opts.buttonActiveClass);
            this.$menu.removeClass(this.opts.menuActiveClass);
        };
    });

    $(window).on('resize.menu', $.rared(function() {
        var winWidth = $.winWidth();
        var winHeight = $.winHeight();
        $.each(menus, function() {
            if (this.$menu.hasClass(this.opts.menuActiveClass)) {
                if (this.opts.fullHeight) {
                    // на всю высоту окна
                    this.$menu.height('auto');
                    var default_height = this.$menu.outerHeight();
                    this.$menu.outerHeight(Math.max(default_height, winHeight));
                }

                this.trigger('resize', winWidth);
            }
        })
    }, 100))
    
    // главное меню
    var initMainMenu = function() {
        window.menu = Menu({
            fullHeight: true
        }).on('resize', function(winWidth) {
            // скрытие на больших экранах
            if (winWidth >= 1024) {
                this.hide();
            }
        });
    };

    $(document).ready(function() {
        var $menu = $('#mobile-menu');
        if ($menu.length) {
            initMainMenu();
            return
        }

        var $placeholder = $('.ajax-cache-block[data-key^="template.cache.mobile-menu"]');
        if ($placeholder.length) {
            $placeholder.on('loaded', function() {
                initMainMenu()
            });
        }
    })

})(jQuery);
