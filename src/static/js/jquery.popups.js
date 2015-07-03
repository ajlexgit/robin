(function($) {

/*
    Плагин модальных окон.

    Может существовать только одно окно. Если осуществляется попытка
    открыть новое окно - оно замещает текущее, включая обработчики событий.

    Высота окна динамическая и зависит от содержимого. Кроме того, окно всегда
    находится в центре экрана.

    Настройки:
        // Классы контейнера окна
        classes: ''

        // Показать тень между сайтом и окном
        overlay: true

        // Поместить UI вне модального окна
        outer_ui: false,

        // HTML или метод, возвращающий содержимое окна
        content: ''

        // HTML или метод, возвращающий дополнительные элементы окна, например кнопку закрытия.
        ui: func()

        // Метод, вызываемый при показе окна.
        // Должен вызвать метод this._defaultBeforeShow();
        show: func()

        // Метод, вызываемый при закрытии окна.
        // Должен вызвать метод this._defaultAfterHide();
        hide: func()

        // Метод, вызываемый при клике вне окна (либо false)
        outClick: func(event)

    Методы объекта окна:
        // Показать окно
        popup.show()

        // Скрыть окно
        popup.hide()

        // Сохраняет значения указанных стилей css1, css2, ... элемента $element.
        popup.saveStyles($element, css1, css2, ...)

        // Восстанавливает ранее сохраненные значения стилей элемента $element.
        popup.loadStyles($element)

    Внутренняя система событий:
        popup.on(events, callback)
        popup.off(events, callback)
        popup.trigger(event, params)

        Где events - это имена событий, разделенных пробелом.
        Ко всем событиям добавляется namespace ".popup"

    Примеры:
        0) Создание и показ пустого окна
            $.popup({}).show();

        1) Показать существующее окно
            $.popup().show();

        2) Закрыть окно:
            $.popup().hide();

        3) Создать окно с содержимым:
            $.popup({
                classes: 'popup-sample',
                content: '<h1>Hello, my friend</h1>'
            }).show();

        4) Заменить содержимое и параметры открытого окна:
            $.popup().update({
                classes: 'new-class',
                content: '<h1>Good bay, my friend</h1>',
            })

        5) Нечто вроде alert:
            $.popup({
                overlay: false,
                content: '<h1>I am alert example</h1>',
                show: function() {
                    this.trigger('before_show');
                    this._defaultBeforeShow();
                    this.trigger('show');
                },
                hide: function() {
                    this.trigger('before_hide');
                    this._defaultAfterHide();
                    this.trigger('hide');
                },
                outClick: $.noop
            }).show()

        6) Загрузка окна через AJAX:
            $.ajax({
                url: '/post/popup/',
                success: function(response) {
                    $.popup({
                        content: response
                    }).show();
                },
                error: function() {
                    $.popup({
                        content: '<h1>Ошибка</h1>'
                    }).show();
                }
            })

        7) Если окно видимо - обновить, иначе - создать и показать
            $.popup.force({
                classes: 'preloader',
                ui: false,
                outClick: false
            });

            $.ajax({
                ...
                success: function(response) {
                    $.popup({
                        content: response
                    });
                },
                ...
            })

    Инфа для разработчика:
        Блок $content введен в $window из-за необходимости разных значений overflow.
*/

    window.Popup = (function() {
        // IDs
        var ID_CONTAINER = 'popup-container';
        var ID_OVERLAY = 'popup-overlay';
        var ID_WINDOW_WRAPPER = 'popup-window-wrapper';
        var ID_WINDOW = 'popup-window';
        var ID_CONTENT = 'popup-content';
        var ID_CLOSE_BUTTON = 'popup-close-button';

        // ===================================================

        var $body = $(document.body);
        var $html = $(document.documentElement);
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

        var DEFAULT_SETTINGS = {
            classes: '',
            overlay: true,
            content: '',
            outer_ui: false,
            clean: true,

            ui: function() {
                var that = this;
                return that._defaultUI();
            },

            show: function() {
                var that = this;
                that.trigger('before_show');
                that._defaultBeforeShow();

                that.$container.css({
                    opacity: 0
                }).animate({
                    opacity: 1
                }, 200, function() {
                    that.trigger('show');
                });
            },

            hide: function() {
                var that = this;
                that.trigger('before_hide');

                that.$container.animate({
                    opacity: 0
                }, 200, function() {
                    that._defaultAfterHide();
                    that.trigger('hide');
                });
            },

            outClick: function() {
                this.hide();
            }
        };

        // ===================================================

        var Popup = function(options) {
            $('#' + ID_CONTAINER).remove();
            $('#' + ID_OVERLAY).remove();

            // Создание DOM
            this.$container = $('<div/>').attr('id', ID_CONTAINER);
            this.$overlay = $('<div/>').attr('id', ID_OVERLAY);
            this.$windowWrapper = $('<div/>').attr('id', ID_WINDOW_WRAPPER);
            this.$window = $('<div/>').attr('id', ID_WINDOW);
            this.$content = $('<div/>').attr('id', ID_CONTENT);
            this.$window.append(this.$content);
            this.$windowWrapper.append(this.$window);
            this.$container.append(this.$windowWrapper);
            $body.append(this.$overlay);
            $body.append(this.$container);


            this.visible = false;

            this.settings = {};
            this.update($.extend(true, {}, DEFAULT_SETTINGS, options));

            // Отвязываем все события
            this.$container.off('.popup');

            // Закрываем окно, если оно открыто
            this._defaultAfterHide();
        };


        // Дополнительные элементы окна по умолчанию
        Popup.prototype._defaultUI = function() {
            var that = this;
            var close_button = $('<div/>').attr('id', ID_CLOSE_BUTTON);
            return close_button.on('click', function() {
                that.hide();
                return false;
            });
        };

        // Действия по умолчания при показе окна
        Popup.prototype._defaultBeforeShow = function() {
            this.$windowWrapper.get(0).scrollTop = 0;

            var styles = this._saveStyles($html, 'overflow', 'paddingRight');
            $html.css({
                overflow: 'hidden',
                paddingRight: (parseInt(styles.paddingRight) || 0) + scrollWidth
            });
        };

        // Действия по умолчания при закрытии окна
        Popup.prototype._defaultAfterHide = function() {
            this.$overlay.stop(true).hide();
            this.$container.stop(true).hide();
            this._loadStyles($html);
        };


        // Показ оверлея, если он разрешен. Иначе - скрытие оверлея
        Popup.prototype._checkOverlay = function() {
            this.$overlay.hide();
            if (this.visible && this.settings.overlay) {
                this.$overlay.show();
            }
        };


        // Сохранение CSS-свойств элемента
        Popup.prototype._saveStyles = function($element) {
            var result = {};
            var props = [].slice.call(arguments, 1);
            for (var i = 0, l = props.length; i < l; i++) {
                result[props[i]] = $element.css(props[i]);
            }

            $element.data('_popup_styles', result);
            return result;
        };

        // Восстановление CSS-свойств элемента
        Popup.prototype._loadStyles = function($element) {
            var result = $element.data('_popup_styles');
            if (!result) return;

            for (var prop in result) {
                if (result.hasOwnProperty(prop)) {
                    $element.css(prop, result[prop]);
                }
            }

            $element.removeData('_popup_styles');
        };


        // Показ окна
        Popup.prototype.show = function() {
            if (this.visible) return;
            this.visible = true;

            this._checkOverlay();
            this.$container.stop(true).show();

            // Вешаем событие на клик вне окна
            var that = this;
            $(document).off('.popup.out').on('click.popup.out', function(event) {
                if ($.isFunction(that.settings.outClick)) {
                    var $target = $(event.target);
                    if (!$target.closest(that.$window).length) {
                        that.settings.outClick.call(that, event);
                    }
                }
            });

            this.settings.show.call(this);
            return this;
        };

        // Скрытие окна
        Popup.prototype.hide = function() {
            if (!this.visible) return;
            this.visible = false;

            $(document).off('.popup.out');

            this.settings.hide.call(this);
            return this;
        };

        // Обновление конфигурации окна
        Popup.prototype.update = function(options) {
            $.extend(true, this.settings, options);

            // Установка класса
            if (typeof options.classes != 'undefined') {
                this.$container.removeClass().addClass(options.classes);
            }

            // Интерфейс
            if (typeof options.ui != 'undefined') {
                var $ui = options.ui;
                if ($.isFunction($ui)) {
                    $ui = $ui.call(this);
                }

                // Очистка $window
                this.$content.detach();
                this.$window.empty().append(this.$content);

                // Очистка $windowWrapper
                this.$window.detach();
                this.$windowWrapper.empty().append(this.$window);

                if (this.settings.outer_ui) {
                    this.$windowWrapper.prepend($ui);
                } else {
                    this.$window.prepend($ui);
                }
            }

            // Содержимое окна
            if (typeof options.content != 'undefined') {
                var $content = options.content;
                if ($.isFunction($content)) {
                    $content = $content.call(this);
                }

                this.$content.empty().append($content);
            }

            // Оверлэй
            if (typeof options.overlay != 'undefined') {
                this._checkOverlay();
            }

            this.trigger('config');
            return this;
        };

        // ===================================================

        // Превращает "keyup click" в "keyup.popup click.popup"
        Popup.prototype._format_events = function(events) {
            events = events.trim().split(/\s+/);
            return events.join('.popup ') + '.popup';
        };

        Popup.prototype.on = function(events) {
            var args = [].slice.call(arguments, 0);
            args[0] = this._format_events(events);

            $.fn.on.apply(this.$container, args);
            return this;
        };

        Popup.prototype.trigger = function(event) {
            var args = [].slice.call(arguments, 0);
            args[0] = this._format_events(event);

            $.fn.trigger.apply(this.$container, args);
            return this;
        };

        Popup.prototype.off = function(events) {
            this.$container.off(events);
            return this;
        };

        return Popup;
    })();


    var popup;
    $.popup = function(options) {
        // $.popup() возвращает текущее окно
        if (!options) return popup;

        // $.popup({ ... }) создает новое окно
        return popup = new Popup(options);
    };

    // Если окно видимо - обновляет, иначе - создает новое.
    // Предназначено для прелоадера
    $.popup.force = function(options) {
        if (popup && popup.visible) {
            return popup.update(options);
        }

        return popup = (new Popup(options)).show();
    };

})(jQuery);