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
        var Cart = function(initial, options) {
            this.settings = $.extend({
                prefix: 'cart',
                onSaveToSession: $.noop,
                onUpdateStorage: $.noop
            }, options);

            this.saveStorage(initial);

            var that = this;
            $(window).off('.cart').on('storage.cart', function(event) {
                var origEvent = event.originalEvent;
                if (origEvent.key == that.settings.prefix) {
                    that.opts.onUpdateStorage.call(that);
                }
            });
        };

        // Получение хранилища заказа из localStorage
        Cart.prototype.getStorage = function() {
            var json = localStorage.getItem(this.settings.prefix) || '{}';
            return $.parseJSON(json);
        };

        // Сохранение заказа в localStorage
        Cart.prototype.saveStorage = function(storage) {
            var json = JSON.stringify(storage || {});
            localStorage.setItem(this.settings.prefix, json);
        };

        // Отправка localStorage на сервер для сохранения в сессии
        Cart.prototype.sendStorage = function(storage) {
            var that = this;

            if (this._sendQuery) {
                this._sendQuery.abort();
            }
            return this._sendQuery = $.ajax({
                url: window.js_storage.save_cart,
                type: 'post',
                data: {
                    cart: storage
                },
                dataType: 'json',
                success: function(response) {
                    if (response.error) {
                        alert(response.error);
                    } else {
                        that.opts.onSaveToSession.call(that, response);
                    }
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
        Cart.prototype.addItem = function(sn, count) {
            var storage = this.getStorage();
            var oldValue = parseInt(storage[sn]) || 0;
            var finalCount = oldValue + Math.max(0, parseInt(count) || 0);
            if (window.js_storage.max_product_count) {
                finalCount = Math.min(finalCount, window.js_storage.max_product_count);
            }
            storage[sn] = finalCount;

            this.saveStorage(storage);
            return this.sendStorage(storage);
        };

        return Cart;
    })();

    window.cart = new Cart();

})(jQuery);