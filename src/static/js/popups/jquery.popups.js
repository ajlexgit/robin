(function($) {

    /*
        Плагин модальных окон.

        В один момент времени может существовать множество окон,
        но видимо всегда только одно окно.
        Текущее видимое окно можно получить через getCurrentPopup();

        Любые элементы с классом Popup.CLOSE_BUTTON_CLASS при клике будут закрывать окно.

        После скрытия окна, оно удаляется из DOM.

        Высота окна динамическая и зависит от содержимого.

        Параметры:
            // Классы контейнера окна
            classes: ''

            // HTML или метод, возвращающий содержимое окна
            content: ''

            // Скорость анимации показа и скрытия окна
            speed: 400

        Методы объекта окна:
            // Показ окна. Возвращает Deferred-объект
            popup.show()

            // Изменение содержимого
            popup.setContent('<h1>Hello</h1>')

            // Скрытие окна. Возвращает Deferred-объект
            popup.hide()

            // Мгновенное уничтожение окна
            popup.destroy()

        События:
            ready   - окно создано и готово к показу
            show    - окно стало видимым
            hide    - окно стало скрытым, но ещё присутствует в DOM

        Примеры:
            // Мгновенное уничтожение окна, открытого в данный момент
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
            popup.on('show', function() {
                console.log('Окно показано')
            }).show();

            // Замена содержимого окна
            popup.setContent('<h1 class="title-h1">Goodbay</h1>');

            // Скрытие окна и уничтожение после завершения анимации
            popup.on('hide', function() {
                console.log('Окно скрыто');
            }).hide();

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

    window.Popup = Class(EventedObject, function Popup(cls, superclass) {
        cls.defaults = {
            classes: '',
            content: '',
            speed: 400,
            easingShow: 'easeInCubic',
            easingHide: 'easeOutCubic'
        };

        cls.CONTAINER_ID = 'popup-container';
        cls.WRAPPER_CLASS = 'popup-wrapper';
        cls.WINDOW_CLASS = 'popup-window';
        cls.CONTENT_CLASS = 'popup-content';
        cls.CLOSE_BUTTON_CLASS = 'close-popup';

        // класс <body>, вешающийся при показе окна
        cls.BODY_OPENED_CLASS = 'popup-opened';


        cls.init = function(options) {
            superclass.init.call(this);

            // настройки
            this.opts = $.extend(true, {}, this.defaults, options);

            this._opened = false;
            this._visible = false;
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this._beforeHide();
            this._showScrollbar();
            this._afterHide();
            superclass.destroy.call(this);
        };

        /*
            Создание DOM
         */
        cls._createDom = function() {
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
            Удаление DOM
         */
        cls._removeDOM = function() {
            $('#' + this.CONTAINER_ID).remove();
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

            this.trigger('ready');
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

        //=======================
        // Показ окна
        //=======================

        /*
            Показ готового окна.
         */
        cls.show = function() {
            // если уже открыто - выходим
            if (this.is_opened()) {
                return this;
            }

            var current = getCurrentPopup();
            if (current) {
                // подмена старого (открытого) окна новым
                current._beforeHide();
                current._hideInstant();
                this._createDom();
                this._postInit();
                this._beforeShow();
                this._showInstant();
            } else {
                // показ нового окна
                this._hideScrollbar();
                this._createDom();
                this._postInit();
                this._beforeShow();
                this._show();
            }

            return this;
        };

        cls._beforeShow = function() {
            currentPopup = this;
            this._opened = true;
        };

        /*
            Анимация показа
         */
        cls._show = function() {
            var that = this;
            this.$container.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easingShow,
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
            this.$container.stop(false, false).show();
            this._afterShow();
        };

        cls._afterShow = function() {
            this._visible = true;

            // кнопки закрытия окна
            var that = this;
            $(document).off('.popup.close').on(touchClick + '.popup.close', '.' + this.CLOSE_BUTTON_CLASS, function() {
                that.hide();
                return false;
            });

            this.trigger('show');
        };

        //=======================
        // Скрытие окна
        //=======================

        /*
            Скрытие открытого окна.
         */
        cls.hide = function() {
            // если уже закрыто - выходим
            if (!this.is_opened()) {
                return this;
            }

            this._beforeHide();
            this._hide();

            return this;
        };

        cls._beforeHide = function() {
            this._visible = false;

            // кнопки закрытия окна
            $(document).off('.popup');
        };

        /*
            Анимация скрытия
         */
        cls._hide = function() {
            var that = this;
            this.$container.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easingHide,
                complete: function() {
                    that._showScrollbar();
                    that._afterHide();
                }
            });
        };

        /*
            Мгновенное скрытие окна.
            Используется в случае замены уже существующего видимого окна.
         */
        cls._hideInstant = function() {
            this.$container.stop(false, false).hide();
            this._afterHide();
        };

        cls._afterHide = function() {
            this._opened = false;
            currentPopup = null;
            this.trigger('hide');
            this._removeDOM();
        };
    });


    /*
        Модальное окно с оверлеем, кнопкой закрытия
     */
    window.OverlayedPopup = Class(window.Popup, function OverlayedPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            closeButton: true,
            hideOnClick: true
        });

        cls.OVERLAY_ID = 'popup-overlay';


        /*
            Создание DOM
         */
        cls._createDom = function() {
            superclass._createDom.call(this);

            this.$overlay = $('<div>').attr('id', this.OVERLAY_ID).hide();
            this.$overlay.addClass(this.opts.classes);
            this.$container.before(this.$overlay);

            if (this.opts.closeButton) {
                this.$closeBtn = $('<div>').addClass(this.CLOSE_BUTTON_CLASS).addClass('popup-close-button');
                this.addCloseButton(this.$closeBtn);
            }
        };

        /*
            Удаление DOM
         */
        cls._removeDOM = function() {
            $('#' + this.OVERLAY_ID).remove();
            superclass._removeDOM.call(this);
        };

        /*
            Добавление кнопки закрытия в DOM
         */
        cls.addCloseButton = function($button) {
            this.$window.prepend($button);
        };

        /*
            Определение того, что клик произошел вне окна и нужно его закрыть (если hideOnClick = true)
         */
        cls.isOutСlick = function($target) {
            return $target.closest(this.$window).length == 0;
        };

        /*
            Закрытие окна при клике вне модального окна
         */
        cls._afterShow = function() {
            superclass._afterShow.call(this);

            var that = this;
            if (this.opts.hideOnClick) {
                $(document).on(touchClick + '.popup', function(evt) {
                    if (that.isOutСlick($(evt.target))) {
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
                easing: this.opts.easingShow
            });
            this.$container.stop(false, false).fadeIn({
                duration: this.opts.speed,
                easing: this.opts.easingShow,
                complete: function() {
                    that._afterShow();
                }
            });
        };

        /*
            Показ окна в случае замены уже существующего
         */
        cls._showInstant = function() {
            this.$overlay.stop(false, false).show();
            superclass._showInstant.call(this);
        };

        /*
            Анимация скрытия
         */
        cls._hide = function() {
            var that = this;
            this.$overlay.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easingHide
            });
            this.$container.stop(false, false).fadeOut({
                duration: this.opts.speed,
                easing: this.opts.easingHide,
                complete: function() {
                    that._showScrollbar();
                    that._afterHide();
                }
            });
        };

        /*
            Скрытие окна в случае замены уже существующего
         */
        cls._hideInstant = function() {
            this.$overlay.stop(false, false).hide();
            superclass._hideInstant.call(this);
        };
    });


    /*
        Алиас создания окна с оверлеем, либо получение текущего окна
     */
    $.popup = function(options) {
        if (options === undefined) {
            return getCurrentPopup();
        } else {
            return window.OverlayedPopup(options);
        }
    };

})(jQuery);
