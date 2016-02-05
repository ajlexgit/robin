(function($) {

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

            beforeShow          - событие перед показом меню. Если вернёт false,
                                  меню не будет показано
            beforeHide          - событие перед скрытием меню. Если вернёт false,
                                  меню не будет скрыто
            onResize            - событие изменения размера окна браузера
    */

    var menus = [];

    var Menu = Class(Object, function Menu(cls, superclass) {
        cls.init = function(options) {
            // настройки
            this.opts = $.extend({
                menuSelector: '#mobile-menu',
                menuActiveClass: 'active',
                buttonSelector: '#mobile-menu-button',
                buttonActiveClass: 'active',

                fullHeight: false,

                beforeShow: $.noop,
                beforeHide: $.noop,
                onResize: $.noop
            }, options);

            // элемент меню
            this.$menu = $(this.opts.menuSelector).first();
            if (!this.$menu.length) {
                return this.raise('menu element not found');
            }

            var that = this;

            // клик на кнопку
            $(document).off('.menu').on(touchClick + '.menu', this.opts.buttonSelector, function() {
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
            if (this.opts.beforeShow.call(this) === false) {
                return false;
            }

            if (this.opts.fullHeight) {
                // на всю высоту окна
                $.winHeight(this.$menu);
            }

            $(this.opts.buttonSelector).addClass(this.opts.buttonActiveClass);
            this.$menu.addClass(this.opts.menuActiveClass);
        };

        /*
            Скрытие меню
         */
        cls.hide = function() {
            if (this.opts.beforeHide.call(this) === false) {
                return false;
            }

            $(this.opts.buttonSelector).removeClass(this.opts.buttonActiveClass);
            this.$menu.removeClass(this.opts.menuActiveClass);
        };

        /*
            Обновление при изменении размера окна
         */
        cls.refresh = function(win_width) {
            if (!this.$menu.hasClass(this.opts.menuActiveClass)) {
                return
            }

            this.opts.onResize.call(this, win_width);
        };
    });

    $(window).on('resize.menu', $.rared(function() {
        $.each(menus, function() {
            if (this.opts.fullHeight) {
                // на всю высоту окна
                $.winHeight(this.$menu);
            }

            this.refresh($(window).width());
        })
    }, 100));


    // главное меню на мобиле
    window.menu = Menu({
        fullHeight: true,
        onResize: function(win_width) {
            if (win_width >= 1024) {
                // скрытие на больших экранах
                this.hide();
            }
        }
    });

})(jQuery);
