(function($) {
    'use strict';

    /*
        Плагин, перемещающий блок в пределах его родителя во время скролла страницы.

        Требует:
            jquery.utils.js, inspectors.js

        Параметры:
            topOffset       - расстояние от верха окна до ползающего блока
            minEnabledWidth - минимальная ширина экрана, при которой блок перемещается

        Пример:
            <div id="block">
                <div class="sticky"></div>
                ...
            </div>

            $(document).ready(function() {
                $('.sticky').sticky();
            });
     */

    var $window = $(window);
    $.widget("django.sticky", {
        options: {
            topOffset: 0,
            minEnabledWidth: 768,

            enable: function(event, data) {
                var that = data.widget;
                that._removeClass(that.element, 'sticky-disabled');
                that._addClass(that.element, 'sticky-enabled');
                that.setElementWidth();
                that.update();
            },
            disable: function(event, data) {
                var that = data.widget;
                that._addClass(that.element, 'sticky-disabled');
                that._removeClass(that.element, 'sticky-enabled');

                that._trigger('state', null, {
                    widget: that,
                    state: 'top'
                });
            },
            state: function(event, data) {
                var that = data.widget;
                var state = data.state;

                if (that._state != state) {
                    that._state = state;

                    that._trigger('update', null, {
                        widget: that,
                        state: state,
                        offset: data.offset
                    });
                }
            },
            update: function(event, data) {
                var that = data.widget;
                var state = data.state;

                if (state == 'top') {
                    that.element.css({
                        position: '',
                        top: ''
                    });
                } else if (state == 'middle') {
                    that.element.css({
                        position: 'fixed',
                        top: that.options.topOffset
                    });
                } else if (state == 'bottom') {
                    that.element.css({
                        position: 'absolute',
                        top: data.offset
                    });
                }
            },
            resize: function(event, data) {
                var that = data.widget;
                that.setElementWidth();
                $.animation_frame(function() {
                    that._update(data.winScroll);
                })(that.element.get(0));
            },
            destroy: function(event, data) {
                var that = data.widget;
                that.element.css({
                    position: '',
                    top: '',
                    width: ''
                });
            }
        },

        _create: function() {
            // нахождение контейнера
            this.block = this._getBlock();

            // стилизация
            this._setStyles();

            // запуск
            this._checkEnabled();

            // Включение и выключение параллакса в зависимости от ширины окна браузера
            var that = this;
            $.mediaInspector.inspect(this.element, {
                point: this.options.minEnabledWidth,
                afterCheck: function($element, opts, state) {
                    var old_state = this.getState($element);
                    if (state === old_state) {
                        return
                    }

                    if (state) {
                        that.enable();
                    } else {
                        that.disable()
                    }
                }
            });
        },

        /*
            Получение элемента контейнера
         */
        _getBlock: function() {
            return this.element.parent();
        },

        /*
            Стилизация
         */
        _setStyles: function() {
            if (this.block.css('position') == 'static') {
                this.block.css({
                    'position': 'relative'
                });
            }
            this.block.css('overflow', 'auto');

            if (!this.element.hasClass('sticky')) {
                this._addClass('sticky');
            }
        },

        /*
            Фиксируем ширину ползающего блока
         */
        setElementWidth: function() {
            var initial_css = this.element.get(0).style.cssText;

            this.element.get(0).style.cssText = '';
            this._width = this.element.width();
            this.element.get(0).style.cssText = initial_css;

            this.element.css('width', this._width);
        },

        /*
            Обновление положения
         */
        update: function() {
            var winScroll = $window.scrollTop();
            this._update(winScroll);
        },

        _update: function(winScroll) {
            if (this.options.disabled) {
                return
            }

            var paddingTop = (parseInt(this.block.css('padding-top')) || 0);
            var paddingBottom = (parseInt(this.block.css('padding-bottom')) || 0);
            var areaHeight = this.block.outerHeight();

            var element_height = this.element.outerHeight(true);

            var scrollFrom = this.block.offset().top + paddingTop - this.options.topOffset;
            var scrollTo = scrollFrom + this.block.height() - element_height;

            if (winScroll < scrollFrom) {
                this._trigger('state', null, {
                    widget: this,
                    state: 'top',
                    offset: 0
                });
            } else if (this.block.height() > this.element.outerHeight(true)) {
                if (winScroll > scrollTo) {
                    this._trigger('state', null, {
                        widget: this,
                        state: 'bottom',
                        offset: areaHeight - element_height - paddingBottom
                    });
                } else if ((winScroll >= scrollFrom) && (winScroll <= scrollTo)) {
                    this._trigger('state', null, {
                        widget: this,
                        state: 'middle',
                        offset: paddingTop + winScroll - scrollFrom
                    });
                }
            }
        },

        _setOptionDisabled: function(value) {
            this._super(value);
            this._checkEnabled();
        },

        _checkEnabled: function() {
            if (this.options.disabled) {
                this._trigger('disable', null, {
                    widget: this
                });
            } else {
                this._trigger('enable', null, {
                    widget: this
                });
            }
        },

        _destroy: function() {
            this.block.css({
                position: '',
                overflow: ''
            });

            this._trigger('destroy', null, {
                widget: this
            });

            $.mediaInspector.ignore(this.element);
        }
    });

    var updateStickies = function() {
        var winScroll = $window.scrollTop();
        $(':django-sticky').each(function() {
            var widget = $(this).sticky('instance');
            $.animation_frame(function() {
                widget._update(winScroll);
            })(widget.element.get(0));
        });
    };

    $window.on('scroll.sticky', updateStickies);
    $window.on('load.sticky', updateStickies);
    $window.on('resize.sticky', $.rared(function() {
        var winScroll = $window.scrollTop();
        $(':django-sticky').each(function() {
            var widget = $(this).sticky('instance');
            widget._trigger('resize', null, {
                widget: widget,
                winScroll: winScroll
            });
        });
    }, 100));

})(jQuery);
