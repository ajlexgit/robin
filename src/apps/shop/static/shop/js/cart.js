(function($) {

    /*
        Корзина продуктов, хранящаюся в localStorage и
        отправляющая запросы на сохранение заказа в сессии.

        Пример:
            cart = new Cart();

            cart.addItem('polovnik', 2).done(function() {
                console.log('saved to session')
            })
     */

    window.Cart = (function() {
        var Cart = function(options) {
            this.opts = $.extend({
                prefix: 'cart',
                onSaveToSession: $.noop,
                onUpdateStorage: $.noop
            }, options);

            var that = this;
            $(window).off('.cart').on('storage.cart', function(event) {
                var origEvent = event.originalEvent;
                if (origEvent.key == that.opts.prefix) {
                    that.opts.onUpdateStorage.call(that);
                }
            });
        };

        // Очистка заказа
        Cart.prototype.clear = function() {
            var that = this;

            localStorage.removeItem(this.opts.prefix);

            if (this._sendQuery) {
                this._sendQuery.abort();
            }
            return this._sendQuery = $.ajax({
                url: window.js_storage.clear_cart,
                type: 'POST',
                dataType: 'json',
                success: function(response) {
                    that.opts.onSaveToSession.call(that, response);
                },
                error: function(xhr, status, error) {
                    if (status != 'abort') {
                        console.error('Error: ' + error + ' (status: ' + status + ')');
                    }
                }
            });
        };

        // Получение хранилища заказа из localStorage
        Cart.prototype.getStorage = function() {
            var json = localStorage.getItem(this.opts.prefix) || '{}';
            return $.parseJSON(json);
        };

        // Сохранение заказа в localStorage
        Cart.prototype.saveStorage = function(storage) {
            var json = JSON.stringify(storage || {});
            localStorage.setItem(this.opts.prefix, json);
        };

        // Отправка localStorage на сервер для сохранения в сессии
        Cart.prototype.sendStorage = function(storage) {
            var that = this;

            if (this._sendQuery) {
                this._sendQuery.abort();
            }
            return this._sendQuery = $.ajax({
                url: window.js_storage.save_cart,
                type: 'POST',
                data: {
                    cart: storage || {}
                },
                dataType: 'json',
                success: function(response) {
                    that.opts.onSaveToSession.call(that, response);
                },
                error: function(xhr, status, error) {
                    if (status != 'abort') {
                        console.error('Error: ' + error + ' (status: ' + status + ')');
                    }
                }
            });
        };

        /*
            Добавление товара в корзину.

            Возвращает Deferred-объект, представляющий AJAX-запрос,
            сохраняющий весь заказ в сессию.
         */
        Cart.prototype.addItem = function(product_id, count) {
            if (!product_id) {
                console.warn('Cart can\'t find product ID');
                return $.Deferred().reject();
            }

            var storage = this.getStorage();
            var oldValue = parseInt(storage[product_id]) || 0;
            var finalCount = oldValue + Math.max(0, parseInt(count) || 0);
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
        Cart.prototype.removeItem = function(product_id) {
            var storage = this.getStorage();
            if (product_id in storage) {
                delete storage[product_id];
            }

            this.saveStorage(storage);
            return this.sendStorage(storage);
        };

        return Cart;
    })();


    window.cart = new Cart();

    // После авторизации заново записываем заказ в сессию
    $(document).on('login.auth.users', function() {
        var storage = cart.getStorage();
        cart.sendStorage(storage);
    });

})(jQuery);