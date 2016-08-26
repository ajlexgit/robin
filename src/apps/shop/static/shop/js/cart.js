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
                localStorage.removeItem(this.opts.prefix);
                $.removeCookie('clear_cart', {path: '/'});
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
            Очистка заказа в localStorage и сессии
         */
        cls.clear = function(options) {
            localStorage.removeItem(this.opts.prefix);
            $.removeCookie('clear_cart', {path: '/'});

            if (this._clearQuery) {
                this._clearQuery.abort();
            }

            var that = this;
            return this._clearQuery = $.ajax($.extend(true, {
                url: window.js_storage.clear_cart,
                type: 'POST',
                dataType: 'json',
                success: function() {
                    that.trigger('clear');
                },
                error: $.parseError()
            }, options));
        };

        /*
            Получение хранилища заказа из localStorage
          */
        cls.getStorage = function() {
            var json = localStorage.getItem(this.opts.prefix);
            try {
                var storage = $.parseJSON(json);
            } catch (err) {
                storage = {}
            }
            return storage || {};
        };

        /*
            Сохранение заказа в localStorage
          */
        cls.saveStorage = function(storage) {
            var json = JSON.stringify(storage || {});
            localStorage.setItem(this.opts.prefix, json);
        };

        /*
            Отправка localStorage на сервер для сохранения в сессии
          */
        cls.sendStorage = function(storage, options) {
            if (this._sendQuery) {
                this._sendQuery.abort();
            }

            var that = this;
            return this._sendQuery = $.ajax($.extend(true, {
                url: window.js_storage.save_cart,
                type: 'POST',
                data: {
                    cart: storage || {}
                },
                dataType: 'json',
                success: function(response) {
                    that.trigger('save', response);
                },
                error: $.parseError()
            }, options));
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
            var finalCount = (parseInt(storage[product_id]) || 0) + count;
            if (window.js_storage.max_product_count) {
                finalCount = Math.min(finalCount, window.js_storage.max_product_count);
            }
            storage[product_id] = finalCount;

            this.saveStorage(storage);
            return this.sendStorage(storage);
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
            }

            var total_count = 0;
            $.each(storage, function(id, count) {
                total_count += count;
            });
            if (!total_count) {
                return this.clear();
            }

            this.saveStorage(storage);
            return this.sendStorage(storage);
        };
    });


    window.cart = window.Cart();

    /*
        После авторизации заново записываем заказ в сессию,
        т.к. ключ сессии изменится.
      */
    $(document).on('login.auth.users logout.auth.users', function() {
        var storage = window.cart.getStorage();
        if (!$.isEmptyObject(storage)) {
            window.cart.sendStorage(storage);
        }
    });

})(jQuery);