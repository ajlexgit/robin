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
            beforeShow          - событие перед показом меню. Если вернёт false,
                                  меню не будет показано
            beforeHide          - событие перед скрытием меню. Если вернёт false,
                                  меню не будет скрыто
            onResize            - событие изменения размера окна браузера
    */

    var menus = [];

    var Menu = Class(null, function Menu(cls, superclass) {
        cls.defaults = {
            menuSelector: '#mobile-menu',
            menuActiveClass: 'active',
            buttonSelector: '#mobile-menu-button',
            buttonActiveClass: 'active',

            beforeShow: $.noop,
            beforeHide: $.noop,
            onResize: $.noop
        };


        cls.init = function(options) {
            // настройки
            this.opts = $.extend({}, this.defaults, options);

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
            if (this.opts.beforeShow.call(this) === false) {
                return false;
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
            this.refresh(window.innerWidth)
        })
    }, 100));


    // главное меню на мобиле
    window.menu = Menu({
        onResize: function(win_width) {
            if (win_width >= 1024) {
                // скрытие на больших экранах
                var $buttons = $(this.opts.buttonSelector);
                $buttons.removeClass(this.opts.buttonActiveClass);
                this.$menu.removeClass(this.opts.menuActiveClass);
            } else {
                // меню на всю высоту на мобилах
                $.winHeight(this.$menu);
            }
        }
    });

})(jQuery);
