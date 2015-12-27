(function($) {

    /*
        Плагин модальных окон.

        Может существовать только одно окно.
        Текущее окно можно получить через getCurrentPopup();

        Высота окна динамическая и зависит от содержимого. Кроме того, окно всегда
        находится в центре экрана.

        Параметры:
            // Классы контейнера окна
            classes: ''

            // HTML или метод, возвращающий содержимое окна
            content: ''

            // Скорость анимации показа и скрытия окна
            speed: 400

            // Событие создания окна
            onInit: function() {}

            // Событие показа окна
            beforeShow: function() {}

            // Событие скрытия окна
            beforeHide: function() {}

        Методы объекта окна:
            // Показ окна. Возвращает Deferred-объект
            popup.show()

            // Изменение содержимого
            popup.setContent('<h1>Hello</h1>')

            // Скрытие окна. Возвращает Deferred-объект
            popup.hide()

            // Мгновенное уничтожение окна
            popup.destroy()

        Примеры:
            // Уничтожение окна, открытого в данный момент
            var current_popup = getCurrentPopup();
            if (current_popup) {
                current_popup.destroy()
            }

            // Создание скрытого окна с оверлеем
            var popup = OverlayedPopup({
                classes: 'my-popup',
                content: '<h1 class="title-h1">Hello</h1>'
            });

            // Создание и показ окна с оверлеем через jQuery-алиас
            $.popup({
                classes: 'overlayed-popup',
                content: '<h1 class="title-h1">Overlayed popup</h1>'
            }).show()


            // Показ окна с выводом сообщения после окончания анимации
            popup.show().done(function() {
                console.log('Окно показано')
            });

            // Замена содержимого окна
            popup.setContent('<h1 class="title-h1">Goodbay</h1>');

            // Скрытие окна и уничтожение после завершения анимации
            popup.hide().done(function() {
                popup.destroy();
            });

        Инфа для разработчика:
            Блок $content введен в $window из-за необходимости разных значений overflow.
    */

    // определение ширины скроллбара
    var scrollWidth = (function() {
        var div = document.createElement('div');
        div.style.position = 'absolute';
        div.style.overflowY = 'scroll';
        div.style.width = '20px';
        div.style.visibility = 'hidden';
        div.style.padding = '0';
        div.style.fontSize = '0';
        div.style.borderWidth = '0';
        document.body.appendChild(div);
        var result = div.offsetWidth - div.clientWidth;
        document.body.removeChild(div);
        return result;
    })();

    // jQuery body
    var $body = $(document.body);

    // текущее окно
    var currentPopup = null;

    /*
        Получение текущего окна
     */
    window.getCurrentPopup = function() {
        return currentPopup;
    };

    window.Popup = Class(null, function Popup(cls, superclass) {
        cls.defaults = {
            classes: '',
            content: '',
            speed: 400,
            easing: 'easeOutCubic',

            onInit: $.noop,
            beforeShow: $.noop,
            beforeHide: $.noop
        };

        cls.CONTAINER_ID = 'popup-container';
        cls.WRAPPER_CLASS = 'popup-wrapper';
        cls.WINDOW_CLASS = 'popup-window';
        cls.CONTENT_CLASS = 'popup-content';

        // класс <body>, вешающийся при показе окна
        cls.BODY_OPENED_CLASS = 'popup-opened';


        cls.init = function(options) {
            // настройки
            this.opts = $.extend(true, {}, this.defaults, options);

            // уничтожение старого окна
            var old_popup = getCurrentPopup();
            if (old_popup) {
                // сохраняем старые параметры, т.к. они потеряются
                old_popup.__opened = old_popup._opened;
                old_popup.__visible = old_popup._visible;
                old_popup.destroy();
            }

            this._createDom();
            this._postInit();

            this._opened = false;
            this._visible = false;

            // замена старого окна
            if (old_popup) {
                // восстанавливаем старые параметры
                old_popup._opened = old_popup.__opened;
                old_popup._visible = old_popup.__visible;
                delete old_popup.__opened;
                delete old_popup.__visible;
                this._replacePopup(old_popup);
            }

            // установка текущего окна
            currentPopup = this;
        };

        /*
            Создание DOM:

            <div id="container">
                <div id="wrapper">
                    <div id="window">
                        <div id="content"></div>
                    </div>
                </div>
            </div>
         */
        cls._createDom = function() {
            $('#' + this.CONTAINER_ID).remove();

            // Создание DOM (изначально скрытого)
            this.$container = $('<div/>').attr('id', this.CONTAINER_ID).hide();
            this.$windowWrapper = $('<div/>').addClass(this.WRAPPER_CLASS);
            this.$window = $('<div/>').addClass(this.WINDOW_CLASS);
            this.$content = $('<div/>').addClass(this.CONTENT_CLASS);

            this.$window.append(this.$content);
            this.$windowWrapper.append(this.$window);
            this.$container.append(this.$windowWrapper);
            $body.append(this.$container);
        };

        /*
            Дополнительная обработка после создания DOM
         */
        cls._postInit = function() {
            // content
            var content;
            if ($.isFunction(this.opts.content)) {
                content = this.opts.content.call(this);
            } else {
                content = this.opts.content;
            }
            this.$content.html(content);

            // classes
            this.$container.addClass(this.opts.classes);

            // callback
            this.opts.onInit.call(this);
        };

        //=======================
        // Скроллбар <body>
        //=======================

        // Есть ли дефолтный скроллбар
        cls._hasScrollBar = function() {
            return document.body.scrollHeight > document.body.clientHeight;
        };

        // Скрытие дефолтного скроллбара
        cls._hideScrollbar = function() {
            var body_padding = parseInt($body.css('paddingRight')) || 0;
            document.body._popup_padding = body_padding;

            $body.addClass(this.BODY_OPENED_CLASS);

            if (this._hasScrollBar()) {
                $body.css({
                    paddingRight: body_padding + scrollWidth
                });
            }
        };

        // Показ дефолтного скроллбара
        cls._showScrollbar = function() {
            if (document.body._popup_padding !== undefined) {
                var body_padding = parseInt(document.body._popup_padding) || 0;
                delete document.body._popup_padding;

                $body.css({
                    paddingRight: body_padding
                });
            }

            $body.removeClass(this.BODY_OPENED_CLASS);
        };

        /*
            Вызывается при создании ногово Popup, когда
            ещё не уничтожен старый.

            На момент вызова, DOM старого окна уже удален,
            а DOM нового уже создан.

            По умолчанию здесь происходит мгновенный показ окна, если прежнее окно было открыто.
         */
        cls._replacePopup = function(old_popup) {
            if (old_popup.is_opened()) {
                this._beforeShow();
                this._showInstant();
            }
        };

        //=======================
        // Методы
        //=======================

        /*
            Установка содержимого. Может быть анимировано
         */
        cls.setContent = function(content) {
            this.$content.empty();
            this.$content.html(content);
        };

        /*
            Открыто ли окно (true до анимации)
         */
        cls.is_opened = function() {
            return this._opened;
        };

        /*
            Видимо ли окно (true после анимации)
         */
        cls.is_visible = function() {
            return this._visible;
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this._beforeHide();
            this._afterHide();
            this.$container.remove();
            currentPopup = null;
        };

        //=======================
        // Показ окна
        //=======================

        /*
            Показ готового окна.
            Возвращает Deferred-объект, который "ресолвится" после
            завершения анимации показа окна.
         */
        cls.show = function() {
            this._deferredShow = $.Deferred();

            if (this.is_opened()) {
                return this._deferredShow.resolve();
            }

            this._beforeShow();
            this._show();

            return this._deferredShow;
        };

        cls._beforeShow = function() {
            this._opened = true;
            this._hideScrollbar();

            // callback
            this.opts.beforeShow.call(this);
        };

        /*
            Анимация показа
         */
        cls._show = function() {
            var that = this;
            this.$container.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    that._afterShow();
                }
            });
        };

        /*
            Мгновенный показ окна.
            Используется в случае замены уже существующего видимого окна.
         */
        cls._showInstant = function() {
            this.$container.show();
            this._afterShow();
        };

        cls._afterShow = function() {
            this._visible = true;
            this._deferredShow && this._deferredShow.resolve();
        };

        //=======================
        // Скрытие окна
        //=======================

        /*
            Скрытие открытого окна.
            Возвращает Deferred-объект, который "ресолвится" после
            завершения анимации скрытия окна.
         */
        cls.hide = function() {
            this._deferredHide = $.Deferred();

            if (!this.is_opened()) {
                return this._deferredHide.resolve();
            }

            this._beforeHide();
            this._hide();

            return this._deferredHide;
        };

        cls._beforeHide = function() {
            this._visible = false;

            // callback
            this.opts.beforeHide.call(this);
        };

        /*
            Анимация скрытия
         */
        cls._hide = function() {
            var that = this;
            this.$container.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    that._afterHide();
                }
            });
        };

        cls._afterHide = function() {
            this._showScrollbar();
            this._opened = false;
            this._deferredHide && this._deferredHide.resolve();
        };
    });


    /*
        Модальное окно с оверлеем, кнопкой закрытия
     */
    window.OverlayedPopup = Class(Popup, function OverlayedPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            closeButton: true,
            hideOnClick: true
        });

        cls.OVERLAY_ID = 'popup-overlay';
        cls.CLOSE_BUTTON_CLASS = 'popup-close-button';


        /*
            Создание DOM
         */
        cls._createDom = function() {
            $('#' + this.OVERLAY_ID).remove();

            superclass._createDom.call(this);

            this.$overlay = $('<div>').attr('id', this.OVERLAY_ID).hide();
            this.$container.before(this.$overlay);

            if (this.opts.closeButton) {
                this.$closeBtn = $('<div>').addClass(this.CLOSE_BUTTON_CLASS);
                this.$window.prepend(this.$closeBtn);

                var that = this;
                this.$closeBtn.on('click.popup', function() {
                    that.hide();
                    return false;
                });
            }
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            superclass.destroy.call(this);
            this.$overlay.remove();
        };

        /*
            Закрытие окна при клике вне модального окна
         */
        cls._beforeShow = function() {
            superclass._beforeShow.call(this);

            var that = this;
            if (this.opts.hideOnClick) {
                $(document).on('click.popup', function(evt) {
                    var $target = $(evt.target);
                    if (!$target.closest(that.$window).length) {
                        that.hide();
                    }
                });
            }
        };

        /*
            Анимация показа
         */
        cls._show = function() {
            var that = this;
            this.$overlay.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easing
            });
            this.$container.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    that._afterShow();
                }
            });
        };

        /*
            Показ окна в случае замены уже существующего
         */
        cls._showInstant = function() {
            this.$overlay.show();
            this.$container.show();
            this._afterShow();
        };

        /*
            Анимация скрытия
         */
        cls._hide = function() {
            var that = this;
            this.$container.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easing
            });
            this.$overlay.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easing,
                complete: function() {
                    that._afterHide();
                }
            });
        };

        /*
            Отвязывание обработчика закрытия окна при клике вне окна
         */
        cls._beforeHide = function() {
            superclass._beforeHide.call(this);
            $(document).off('click.popup');
        };
    });


    /*
        Алиас создания окна с оверлеем, либо получение текущего окна
     */
    $.popup = function(options) {
        if (options === undefined) {
            return getCurrentPopup();
        } else {
            return OverlayedPopup(options);
        }
    };

})(jQuery);
