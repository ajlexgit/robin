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

            // клик на кнопку
            var that = this;
            $(document).off('.menu').on('click.menu', this.opts.buttonSelector, function() {
                return that.onClick($(this));
            });

            menus.push(this);
        };

        /*
            Обработчик нажатия кнопки
         */
        cls.onClick = function($button) {
            var $menu = $(this.opts.menuSelector).first();
            if (!$menu.length) {
                this.error('menu element not found');
                return false;
            }

            var currently_active = $button.hasClass(this.opts.buttonActiveClass);
            if (currently_active) {
                this.hide($menu)
            } else {
                this.show($menu)
            }

            return false;
        };

        cls.update = function($menu) {
            // на всю высоту окна
            if (this.opts.fullHeight) {
                $menu.height('auto');
                var default_height = $menu.outerHeight();
                $menu.outerHeight(Math.max(default_height, $.winHeight()));
            }
        };

        /*
            Показ меню
         */
        cls.show = function($menu) {
            if (this.trigger('before_show') === false) {
                return false;
            }

            this.update($menu);
            $(this.opts.buttonSelector).addClass(this.opts.buttonActiveClass);
            $menu.addClass(this.opts.menuActiveClass);
        };

        /*
            Скрытие меню
         */
        cls.hide = function($menu) {
            if (this.trigger('before_hide') === false) {
                return false;
            }

            $(this.opts.buttonSelector).removeClass(this.opts.buttonActiveClass);
            $menu.removeClass(this.opts.menuActiveClass);
        };
    });

    $(window).on('resize.menu', $.rared(function() {
        var winWidth = $.winWidth();
        $.each(menus, function() {
            var $menu = $(this.opts.menuSelector).first();
            if (!$menu.hasClass(this.opts.menuActiveClass)) {
                return
            }

            this.update($menu);
            this.trigger('resize', winWidth);
        })
    }, 100));

    $(document).ready(function() {
        window.menu = Menu({
            fullHeight: true
        }).on('resize', function(winWidth) {
            // скрытие на больших экранах
            if (winWidth >= 1024) {
                this.hide();
            }
        });
    })

})(jQuery);
