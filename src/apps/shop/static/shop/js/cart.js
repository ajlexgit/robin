(function($) {

    /*
        Корзина продуктов, которая хранится в localStorage и
        отправляющая запросы на сохранение заказа в сессии.

        Требует:
            jquery.utils.js

        Параметры:
            prefix      - префикс хранилища localStorage

        События:
            // после сохранения в сессии
            save(response)

            // при изменении заказа в localStorage (из другой вкладки)
            update()

            // при очистке корзины
            clear()

        Пример:
            // добавить два товара с ID 78
            cart.addItem(78, 2).done(function() {
                console.log('saved to session')
            })
     */

    window.Cart = Class(EventedObject, function Cart(cls, superclass) {
        cls.defaults = {
            prefix: 'cart'
        };

        cls.init = function(options) {
            superclass.init.call(this);
            this.opts = $.extend({}, this.defaults, options);

            // очистка корзины в localStorage, если стоит кука
            var force_clean = $.cookie('clear_cart');
            if (force_clean) {
                this._clearLocal();
                this.trigger('clear');
            }

            var that = this;
            $(window).off('.cart').on('storage.cart', function(event) {
                var origEvent = event.originalEvent;
                if (origEvent.key == that.opts.prefix) {
                    that.trigger('update');
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
            $.removeCookie('clear_cart', {path: '/'});
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
            var storage = this.getStorage();
            return $.isEmptyObject(storage);
        };

        /*
            Сохранение заказа в localStorage и в сессию
          */
        cls.saveStorage = function(storage) {
            storage = this._formatStorage(storage);

            if (this._query) {
                this._query.abort();
            }

            var that = this;
            if ($.isEmptyObject(storage)) {
                // корзина пуста
                this._clearLocal();

                return this._query = $.ajax({
                    url: window.js_storage.clear_cart,
                    type: 'POST',
                    dataType: 'json',
                    success: function() {
                        that.trigger('clear');
                    },
                    error: $.parseError()
                });
            } else {
                // корзина не пуста
                this._saveToLocal(storage);

                return this._query = $.ajax({
                    url: window.js_storage.save_cart,
                    type: 'POST',
                    data: {
                        cart: storage
                    },
                    dataType: 'json',
                    success: function(response) {
                        that.trigger('save', response);
                    },
                    error: $.parseError()
                });
            }
        };

        /*
            Обновление корзины в localStorage из сессии
          */
        cls.loadStorage = function() {
            var that = this;
            return $.ajax({
                url: window.js_storage.load_cart,
                type: 'GET',
                dataType: 'json',
                success: function(response) {
                    that.saveStorage(response.cart);
                },
                error: $.parseError()
            });
        };

        /*
            Добавление товара в корзину.

            Возвращает Deferred-объект, представляющий AJAX-запрос,
            сохраняющий весь заказ в сессию.
         */
        cls.addItem = function(product_id, count) {
            if (!product_id) {
                this.error('product ID required');
                return $.Deferred().reject();
            }

            count = Math.max(0, parseInt(count) || 0);
            if (!count) {
                this.error('zero count');
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

            Возвращает Deferred-объект, представляющий AJAX-запрос,
            сохраняющий весь заказ в сессию.
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


    window.cart = window.Cart();

    /*
        После авторизации заново записываем заказ в сессию,
        т.к. ключ сессии изменится.
      */
    $(document).on('login.auth.users logout.auth.users', function() {
        if (!window.cart.isEmpty()) {
            var storage = window.cart.getStorage();
            window.cart.saveStorage(storage);
        }
    });

})(jQuery);