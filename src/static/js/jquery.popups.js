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

        // Содержимое окна
        content: ''

        // Очистить элементы окна от классов и inline-стилей
        clean: true

        // Метод, возвращающий дополнительные элементы окна, например кнопку закрытия.
        ui: func(internal)

        // Метод, вызываемый при popup.show(). Принимает callback-функцию internal,
        // которая выполняет действия по умолчанию.
        show: func(internal)

        // Метод, вызываемый при popup.hide(). Принимает callback-функцию internal,
        // которая выполняет действия по умолчанию.
        hide: func(internal)

        // Метод, вызываемый при клике вне окна. Принимает объект события.
        outClick: func(event)

    Методы объекта окна:
        // Показать окно
        popup.show()

        // Скрыть окно
        popup.hide()

        // Сохраняет значения указанных стилей css1, css2, ... элемента $element.
        popup.saveStyles($element, css1, css2, ...)

        // Восстанавливает ранее сохраненные значения указанных стилей элемента $element.
        popup.loadStyles($element, css1, css2, ...)

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
                show: function(internal) {
                    internal.call(this)
                },
                hide: function(internal) {
                    internal.call(this)
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
                content: '<h1>I am alert example</h1>',
            })

    Инфа для разработчика:
        Блок $content введен в $window из-за необходимости разных значений overflow.
*/

    var popup,
        scrollWidth = (function() {
            var div = document.createElement('div');
            div.style.position = 'absolute';
            div.style.overflowY = 'scroll';
            div.style.width =  '20px';
            div.style.visibility = 'hidden';
            div.style.padding = '0';
            div.style.fontSize = '0';
            div.style.borderWidth = '0';
            document.body.appendChild(div);
            var result = div.offsetWidth - div.clientWidth;
            document.body.removeChild(div);
            return result;
        })();

    var ID_CONTAINER = 'popup-container',
        ID_OVERLAY = 'popup-overlay',
        ID_WINDOW_WRAPPER = 'popup-window-wrapper',
        ID_WINDOW = 'popup-window',
        ID_CONTENT = 'popup-content';


    var Popup = function() {
        var that =this;
        var $body = $(document.body);
        this.visible = false;

        this.internal = {
            ui: function() {
                var close_button = $('<div/>').attr('id', 'popup-close-button');
                return close_button.on('click', function() {
                    that.hide();
                    return false;
                });
            },
            show: function() {
                that.$windowWrapper.get(0).scrollTop = 0;
                var $html = $(document.documentElement),
                    saved = that.saveStyles($html, 'overflow', 'paddingRight');
                $html.css({
                    overflow: 'hidden',
                    paddingRight: (parseInt(saved.paddingRight) || 0) + scrollWidth
                });
            },
            hide: function() {
                that._overlay();
                that.$container.stop(true).hide();
                that.loadStyles($(document.documentElement), 'overflow', 'paddingRight');
            }
        };

        // Сохранение CSS свойств элемента
        this.saveStyles = function($element) {
            var storage = $element.data(),
                props = [].slice.call(arguments, 1),
                result = {};
            for (var i=0, l=props.length; i<l; i++) {
                var storage_name = '_popup_'+props[i];
                if (typeof storage[storage_name] == 'undefined') {
                    storage[storage_name] = result[props[i]] = $element.css(props[i]);
                }
            }
            return result;
        };

        // Восстановление CSS свойств элемента
        this.loadStyles = function($element) {
            var storage = $element.data(),
                props = [].slice.call(arguments, 1);
            for (var i=0, l=props.length; i<l; i++) {
                var storage_name = '_popup_'+props[i];
                if (typeof storage[storage_name] != 'undefined') {
                    $element.css(props[i], storage[storage_name]);
                    delete storage[storage_name];
                }
            }
        };


        // Показ окна
        this.show = function() {
            if (this.visible) return;
            this.visible = true;
            this._overlay();
            this.$container.stop(true).show();
            this.__show.call(this, this.internal.show);
            return this;
        };

        // Скрытие окна
        this.hide = function() {
            if (!this.visible) return;
            this.visible = false;
            this.__hide.call(this, this.internal.hide);
            return this;
        };

        // ============================

        // Показ оверлея, если окно открыто и видимо. Иначе - скрытие оверлея
        this._overlay = function() {
            this.$overlay.hide();
            if (this.visible && this._useOverlay) {
                this.$overlay.show();
            }
        };

        // Инициализация
        this._init = function(settings) {
            this.$container = $('#' + ID_CONTAINER);
            this.$overlay = $('#' + ID_OVERLAY);
            this.$windowWrapper = $('#' + ID_WINDOW_WRAPPER);
            this.$window = $('#' + ID_WINDOW);
            this.$content = $('#' + ID_CONTENT);

            if (!this.$container.length) {
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
            }

            this.update(settings);

            // Отвязываем все события
            this.$container.off('.popup');

            if (!this.visible) {
                this.$container.hide();
            }

            $(document).off('.popup.out').on('click.popup.out', function(event) {
                if (!popup) return;
                if (!$(event.target).closest(popup.$window).length) {
                    popup.__outClick.call(popup, event);
                }
            });

            return this;
        };

        // Применение параметров конфигурации
        this.update = function(settings) {
            var value;

            if (settings.clean) {
                this.$container.removeClass().css('cssText', '');
                this.$overlay.removeClass().css('cssText', '');
                this.$windowWrapper.removeClass().css('cssText', '');
                this.$window.removeClass().css('cssText', '');
                this.$content.removeClass().css('cssText', '');
            }

            // Установка класса
            if (typeof settings.classes != 'undefined') {
                this.$container.removeClass().addClass(settings.classes);
            }

            // Интерфейс
            if (typeof settings.ui != 'undefined') {
                if ($.isFunction(settings.ui)) {
                    value = settings.ui.call(this, this.internal.ui);
                } else {
                    value = settings.ui;
                }
                if (settings.outer_ui) {
                    this.$window.siblings().remove();
                    this.$windowWrapper.prepend(value);
                } else {
                    this.$content.siblings().remove();
                    this.$window.prepend(value);
                }
            }

            // Содержимое
            if (typeof settings.content != 'undefined') {
                if ($.isFunction(settings.content)) {
                    value = settings.content.call(this);
                } else {
                    value = settings.content;
                }
                this.$content.empty();
                this.$content.append(value);
            }

            // Оверлэй
            if (typeof settings.overlay != 'undefined') {
                this._useOverlay = settings.overlay;
                this._overlay();
            }

            // Показ окна
            if (typeof settings.show != 'undefined') {
                this.__show = settings.show;
            }

            // Скрытие окна
            if (typeof settings.hide != 'undefined') {
                this.__hide = settings.hide;
            }

            // Клик вне окна
            if (typeof settings.outClick != 'undefined') {
                this.__outClick = settings.outClick;
            }

            this.trigger('config');
            return this;
        };

        // Навешивание событий
        var format_events = function(events) {
            events = events.trim().split(/\s+/);
            return events.join('.popup ') + '.popup';
        };
        this.on = function(events) {
            var args = [].slice.call(arguments, 0);
            args[0] = format_events(events);
            $.fn.on.apply(this.$container, args);
            return this;
        };
        this.trigger = function(event) {
            var args = [].slice.call(arguments, 0);
            args[0] = format_events(event);
            $.fn.trigger.apply(this.$container, args);
            return this;
        };
        this.off = function(events) {
            this.$container.off(events);
            return this;
        }
    };

    $.popup = function(options) {
        if (typeof options == 'undefined') return popup;
        popup = popup ? popup : new Popup;

        var settings = $.extend(true, {}, $.popup.defaults, options);
        return popup._init(settings);
    };

    // Если окно видимо - обновляет, иначе - создает новое.
    // Предназначено для прелоадера
    $.popup.force = function(options) {
        popup = popup ? popup : new Popup;
        if (popup.visible) {
            return popup.update(options)
        } else {
            var settings = $.extend(true, {}, $.popup.defaults, options);
            return popup._init(settings).show();
        }
    };

    $.popup.defaults = {
        classes: '',
        overlay: true,
        content: '',
        outer_ui: false,
        clean: true,
        ui: function(internal) {
            return internal.call(this);
        },
        show: function(internal) {
            var that = this;
            that.trigger('before_show');
            internal.call(that);
            that.$container.css({
                opacity: 0
            }).animate({
                opacity: 1
            }, 200, function() {
                that.trigger('show');
            });
        },
        hide: function(internal) {
            var that = this;
            that.trigger('before_hide');
            that.$container.animate({
                opacity: 0
            }, 200, function() {
                internal.call(that);
                that.trigger('hide');
            });
        },
        outClick: function() {
            this.hide();
        }
    };

})(jQuery);