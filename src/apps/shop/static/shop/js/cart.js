(function($) {

    /*
        Корзина продуктов, которая хранится в localStorage (для фронтенда) и
        отправляющая AJAX-запросы на сохранение заказа в сессии (для бэкенда).

        Требует:
            jquery.utils.js

        Параметры:
            prefix      - префикс хранилища localStorage

        События:
            // после сохранения в сессии
            save(response)

            // при изменении заказа в localStorage из другой вкладки
            update()

            // при очистке корзины
            clear(response)

        Пример:
            // добавить в корзину два товара с ID 78
            cart.addItem(78, 2).done(function() {
                console.log('saved to session')
            })


            // обновление блока корзины после сохранения в сессию
            window.cart.on('save', function(response) {
                if (response.cart_block) {
                    $('.cart-block').replaceWith(response.cart_block);
                }
            }).on('clear', function(response) {
                if (response.cart_block) {
                    $('.cart-block').replaceWith(response.cart_block);
                }
            });
     */

    /** @namespace window.js_storage */
    /** @namespace window.js_storage.save_cart */
    /** @namespace window.js_storage.load_cart */
    /** @namespace window.js_storage.clear_cart */
    /** @namespace window.js_storage.max_product_count */
    /** @namespace window.js_storage.session_cart_empty */

    var saving_query;
    var loading_query;

    window.Cart = Class(EventedObject, function Cart(cls, superclass) {
        cls.defaults = {
            prefix: 'cart'
        };

        cls.init = function(options) {
            superclass.init.call(this);
            this.opts = $.extend({}, this.defaults, options);

            // ключ параметра localStorage, инициирующего обновление корзины
            // в текущей вкладе, при изменении в другой вкладке
            this._update_trigger = this.opts.prefix + '_state';

            // очистка, вызваннная бэкендом
            var that = this;

            var force_clean = $.cookie('clear_cart');
            if (force_clean) {
                this._clearLocal();
                this._clearSession().done(function(response) {
                    that._updateTabs();
                    that.trigger('clear', response);
                });
            }

            // событие обновления localStorage из другой вкладки
            $(window).on('storage.cart', function(event) {
                if (event.originalEvent.key == that._update_trigger) {
                    var value = localStorage.getItem(that._update_trigger);
                    if (value != null) {
                        that.trigger('update');
                    }
                }
            });
        };

        /*
            Форматирование корзины.
            Допустимы только числовые ключи (больше 0) и такие же значения.
         */
        cls._formatStorage = function(storage) {
            var result = {};
            $.each(storage || {}, function(key, value) {
                key = parseInt(key) || 0;
                if (key <= 0) return;

                value = parseInt(value) || 0;
                if (value <= 0) return;

                result[key] = value;
            });
            return result
        };

        /*
            Получение корзины из localStorage
         */
        cls._getLocal = function() {
            var json = localStorage.getItem(this.opts.prefix);
            try {
                var storage = $.parseJSON(json);
            } catch (err) {
                storage = {}
            }
            return storage || {};
        };

        /*
            Сохранение корзины в localStorage
         */
        cls._saveToLocal = function(storage) {
            var json = JSON.stringify(storage || {});
            localStorage.setItem(this.opts.prefix, json);
        };

        /*
            Очистка корзины в localStorage
         */
        cls._clearLocal = function() {
            localStorage.removeItem(this.opts.prefix);
            localStorage.removeItem(this._update_trigger);

            var cookie_options = {path: '/'};
            if (window.js_storage.cookie_domain) {
                cookie_options['domain'] = window.js_storage.cookie_domain;
            }
            $.removeCookie('clear_cart', cookie_options);
        };

        /*
            Сохранение корзины в сессию
         */
        cls._saveToSession = function(formatted_storage) {
            if (saving_query) {
                saving_query.abort();
            }

            return saving_query = $.ajax({
                url: window.js_storage.save_cart,
                type: 'POST',
                data: {
                    cart: formatted_storage
                },
                dataType: 'json',
                error: $.parseError()
            });
        };

        /*
            Загрузка корзины из сессии
          */
        cls._loadFromSession = function() {
            if (loading_query) {
                loading_query.abort();
            }

            return loading_query = $.ajax({
                url: window.js_storage.load_cart,
                type: 'GET',
                dataType: 'json',
                error: $.parseError()
            });
        };

        /*
            Очистка корзины в сесcии
         */
        cls._clearSession = function() {
            if (saving_query) {
                saving_query.abort();
            }

            return saving_query = $.ajax({
                url: window.js_storage.clear_cart,
                type: 'POST',
                dataType: 'json',
                error: $.parseError()
            });
        };

        /*
            Инициализация обновления корзины в других вкладках
         */
        cls._updateTabs = function() {
            var current_state = localStorage.getItem(this._update_trigger);
            current_state = parseInt(current_state) || 0;
            localStorage.setItem(this._update_trigger, ++current_state);
        };



        /*
            Получение хранилища заказа из localStorage
          */
        cls.getStorage = function() {
            var storage = this._getLocal();
            return this._formatStorage(storage);
        };

        /*
            Проверка localStorage на пустоту
          */
        cls.isEmpty = function() {
            var formatted_storage = this.getStorage();
            return $.isEmptyObject(formatted_storage);
        };

        /*
            Сохранение заказа в localStorage и в сессию.
            Возвращает Deferred-объект, представляющий AJAX-запрос.
          */
        cls.saveStorage = function(storage) {
            var that = this;
            var formatted_storage = this._formatStorage(storage);
            if ($.isEmptyObject(formatted_storage)) {
                // очистка корзины
                this._clearLocal();
                return this._clearSession().done(function(response) {
                    that._updateTabs();
                    that.trigger('clear', response);
                });
            } else {
                // сохранение корзины
                this._saveToLocal(formatted_storage);
                return this._saveToSession(formatted_storage).done(function(response) {
                    that._updateTabs();
                    that.trigger('save', response);
                });
            }
        };

        /*
            Добавление товара в корзину.
            Возвращает Deferred-объект, представляющий AJAX-запрос.
         */
        cls.addItem = function(product_id, count) {
            if (!product_id) {
                this.error('product ID required');
                return $.Deferred().reject();
            }

            count = Math.max(0, parseInt(count) || 0);
            if (!count) {
                this.error('count required');
                return $.Deferred().reject();
            }

            var storage = this.getStorage();
            var new_count = (parseInt(storage[product_id]) || 0) + count;
            if (window.js_storage.max_product_count) {
                new_count = Math.min(new_count, window.js_storage.max_product_count);
            }
            storage[product_id] = new_count;

            return this.saveStorage(storage);
        };

        /*
            Удаление товара из корзины.
            Возвращает Deferred-объект, представляющий AJAX-запрос.
         */
        cls.removeItem = function(product_id) {
            var storage = this.getStorage();
            if (product_id in storage) {
                delete storage[product_id];
                return this.saveStorage(storage);
            } else {
                return $.Deferred().resolve();
            }
        };
    });


    window.cart = window.Cart({

    }).on('update', function() {
        // при изменении корзины из другой вкладки - обновляем страницу
        location.reload(true);
    });


    $(document).on('click', '.add-to-cart-btn', function() {
        // кнопка добавления продукта в корзину
        var product_id = $(this).data('product');
        window.cart.addItem(product_id, 1);
    }).ready(function() {
        // запись корзины в сессию, если localStorage не пуст, а сессия пуста.
        var storage = window.cart.getStorage();
        if (!$.isEmptyObject(storage) && window.js_storage.session_cart_empty) {
            window.cart.saveStorage(storage);
        }
    });

})(jQuery);