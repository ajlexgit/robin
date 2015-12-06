(function($) {

    /*
        Корзина продуктов, хранящаюся в localStorage и
        отправляющая запросы на сохранение заказа в сессии.

        Пример:
            cart = Cart.create();

            // добавить два товара с ID 78
            cart.addItem(78, 2).done(function() {
                console.log('saved to session')
            })
     */

    window.Cart = Class(null, function Cart(cls, superclass) {
        cls.prototype.init = function(options) {
            this.opts = $.extend({
                prefix: 'cart',
                onSave: $.noop,
                onUpdate: $.noop,
                onClear: $.noop
            }, options);

            var force_clean = $.cookie('clear_cart');
            if (force_clean) {
                localStorage.removeItem(this.opts.prefix);
                $.removeCookie('clear_cart', {path: '/'});
            }

            var that = this;
            $(window).off('.cart').on('storage.cart', function(event) {
                var origEvent = event.originalEvent;
                if (origEvent.key == that.opts.prefix) {
                    that.opts.onUpdate.call(that);
                }
            });
        };

        /*
            Очистка заказа
         */
        cls.prototype.clear = function() {
            var that = this;

            localStorage.removeItem(this.opts.prefix);

            if (this._clearQuery) {
                this._clearQuery.abort();
            }
            return this._clearQuery = $.ajax({
                url: window.js_storage.clear_cart,
                type: 'POST',
                dataType: 'json',
                success: function(response) {
                    that.opts.onClear.call(that, response);
                },
                error: function(xhr, status, error) {
                    if (status != 'abort') {
                        console.error('Error: ' + error + ' (status: ' + status + ')');
                    }
                }
            });
        };

        /*
            Получение хранилища заказа из localStorage
          */
        cls.prototype.getStorage = function() {
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
        cls.prototype.saveStorage = function(storage) {
            var json = JSON.stringify(storage || {});
            localStorage.setItem(this.opts.prefix, json);
        };

        /*
            Отправка localStorage на сервер для сохранения в сессии
          */
        cls.prototype.sendStorage = function(storage, options) {
            var that = this;

            if (this._sendQuery) {
                this._sendQuery.abort();
            }

            var ajax_options = $.extend(true, {
                url: window.js_storage.save_cart,
                type: 'POST',
                data: {
                    cart: storage || {}
                },
                dataType: 'json',
                success: function(response) {
                    that.opts.onSave.call(that, response);
                },
                error: function(xhr, status, error) {
                    if (status != 'abort') {
                        console.error('Error: ' + error + ' (status: ' + status + ')');
                    }
                }
            }, options);

            return this._sendQuery = $.ajax(ajax_options);
        };

        /*
            Добавление товара в корзину.

            Возвращает Deferred-объект, представляющий AJAX-запрос,
            сохраняющий весь заказ в сессию.
         */
        cls.prototype.addItem = function(product_id, count) {
            if (!product_id) {
                this.error('product ID required');
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
        cls.prototype.removeItem = function(product_id) {
            var storage = this.getStorage();
            if (product_id in storage) {
                delete storage[product_id];
            }

            this.saveStorage(storage);
            return this.sendStorage(storage);
        };
    });

    // После авторизации заново записываем заказ в сессию
    $(document).on('login.auth.users logout.auth.users', function() {
        var storage = cart.getStorage();
        if (!$.isEmptyObject(storage)) {
            cart.sendStorage(storage);
        }
    });

    window.cart = Cart.create();

})(jQuery);