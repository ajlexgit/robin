(function($) {

    /*
        Плагин, имитирующий у блока поведение ссылки.
        Ссылка должна находиться внутри блока.

        Зависит от:
            jquery-ui.js

        Параметры:
            itemSelector  - селектор блока, который будет имитировать ссылку
            linkSelector  - селектор ссылки внутри блока

        Пример:
            <div class="block">
              <div class="item">
                <a href="..." class="my-link"></a>
              </div>
              <div class="item">
                <a href="..." class="my-link"></a>
              </div>
            </div>


            $('.block').fakeLink({
                itemSelector: '.item',
                linkSelector: '.my-link'
            });
     */

    $.widget("django.fakeLink", {
        options: {
            itemSelector: null,
            linkSelector: 'a',

            enable: $.noop,
            disable: $.noop,
            destroy: $.noop,
            click: $.noop
        },

        _create: function() {
            // нахождение блока и ссылки блока
            this.block = this._getBlock();
            this.link = this._getBlockLink();
            if (!this.link.length || ! this.block.length) {
                return;
            }

            // запуск
            this._checkEnabled();

            // клик на блок
            var that = this;
            this._on(this.block, {
                click: function(event) {
                    if ((event.target === that.link.get(0)) ||
                        ($.contains(that.link.get(0), event.target))) {
                        // клик на целевую ссылку в блоке
                        that._trigger('click', event, {
                            widget: that
                        });
                    } else if ((event.target.tagName === 'A') ||
                        ($.contains(that.block.get(0), $(event.target).closest('a').get(0)))) {
                        // клик на нецелевую ссылку в блоке

                    } else {
                        // клик на блок
                        that._trigger('click', event, {
                            widget: that
                        });

                        var fake_event = new MouseEvent('click', {
                            button: event.button,
                            faked: true,
                            bubbles: true
                        });
                        that.link.get(0).dispatchEvent(fake_event);
                        if (!event.faked) {
                            return false;
                        }
                    }
                },
                mousedown: function(event) {
                    if (event.which === 2) {
                        return false;
                    }
                },
                mouseup: function(event) {
                    if (event.which === 2) {
                        that._trigger('click', event, {
                            widget: that
                        });
                        that.link.get(0).dispatchEvent(new MouseEvent('click', {
                            button: 1
                        }));
                    }
                }
            });
        },

        /*
            Поиск блока
         */
        _getBlock: function() {
            if (this.options.itemSelector) {
                return this.element.find(this.options.itemSelector).first();
            } else {
                return this.element
            }
        },

        /*
            Поиск ссылки блока
         */
        _getBlockLink: function() {
            return this.element.find(this.options.linkSelector).first();
        },

        _setOptionDisabled: function(value) {
            this._super(value);
            this._checkEnabled();
        },

        _checkEnabled: function() {
            if (this.options.disabled) {
                this.trigger('disable');
                this._removeClass(this.block, 'fakelink-item');
            } else {
                this._addClass(this.block, 'fakelink-item');
                this.trigger('enable');
            }
        },

        _destroy: function() {
            this.trigger('destroy');
        },

        /*
            Вызов событий
         */
        trigger: function(type, data) {
            this._trigger(type, null, $.extend({
                widget: this
            }, data));
        }
    });

})(jQuery);
