(function() {
    'use strict';

    /*
        Параллакс-эффект для блока.

        Требует:
            jquery-ui.js, jquery.utils.js, bg_inspector.js, media_inspector.js

        Параметры:
            imageSelector       - селектор выбора элемента, который будет перемещаться
            imageHeightPercents - высота фоновой картинки в процентах относительно высоты блока
            easing              - функция сглаживания перемещения фона
            minEnabledWidth     - минимальная ширина экрана, при которой элемент перемещается

        Пример:
            <div id="block">
                <img class="parallax" src="/img/bg.jpg">
                ...
            </div>

            $(document).ready(function() {
                $('#block').parallax();
            });
     */

    var $window = $(window);
    $.widget("django.parallax", {
        options: {
            imageSelector: '> img',
            imageHeightPercents: 150,
            easing: 'easeInOutQuad',
            minEnabledWidth: 768,

            imageloaded: function(event, data) {
                var that = data.widget;
                that.image.css({
                    minHeight: that.options.imageHeightPercents + '%'
                });
                that._addClass(that.image, 'parallax-image-loaded');
            },
            update: function(event, data) {
                var that = data.widget;
                var backgroundOffset = data.progress * (that.options.imageHeightPercents - 100);
                that.image.css({
                    top: -backgroundOffset + '%'
                });
            }
        },

        _create: function() {
            this.image = this._getImage();
            if (!this.image.length) {
                console.error();
            }

            this._setBlockStyles();
            this._setImageStyles();
            this._updateEnabled();

            // Включение и выключение параллакса в зависимости
            // от ширины окна браузера
            var that = this;
            $.mediaInspector.inspect(this.element, {
                point: this.options.minEnabledWidth,
                afterCheck: function($block, opts, state) {
                    var old_state = this.getState($block);
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

            // инспектирование пропорций
            $.bgInspector.inspect(this.image, {
                checkOnInit: false,
                afterCheck: function($element, opts, state) {
                    if (state) {
                        // картинка шире
                        if (that._enabled) {
                            $element.css({
                                width: '',
                                height: that.options.imageHeightPercents + '%'
                            })
                        } else {
                            $element.css({
                                width: '',
                                height: '100.5%'
                            })
                        }
                    } else {
                        // картинка выше
                        if (that._enabled) {
                            var $parent = $element.parent();
                            var elem_asp = $element.data('bginspector_aspect');
                            var parent_asp = $parent.data('bginspector_aspect');

                            var relation = 100 * (parent_asp / elem_asp);
                            if (relation > that.options.imageHeightPercents) {
                                $element.css({
                                    width: '100.5%',
                                    height: ''
                                })
                            } else {
                                $element.css({
                                    width: 100 * that.options.imageHeightPercents / relation + '%',
                                    height: ''
                                })
                            }
                        } else {
                            $element.css({
                                width: '100.5%',
                                height: ''
                            })
                        }
                    }
                }
            });

            // Вызов инспектора после загрузки картинки
            this.image.onLoaded(true, function() {
                that._trigger('imageloaded', null, {
                    widget: that
                });
                $.bgInspector.check(that.image);
            });
        },

        /*
            Добавление стилей блоку
         */
        _setBlockStyles: function() {
            if (this.element.css('position') == 'static') {
                this.element.css({
                    'position': 'relative'
                })
            }
            this.element.css('overflow', 'hidden');
        },

        /*
            Поиск элемента фонового изображения
         */
        _getImage: function() {
            return this.element.find(this.options.imageSelector);
        },

        /*
            Добавление стилей фоновому изображению
         */
        _setImageStyles: function() {
            if (!this.image.hasClass('parallax-image')) {
                this._addClass(this.image, 'parallax-image');
            }
        },

        /*
            Обновление положения изображения
         */
        update: function() {
            var winScroll = $window.scrollTop();
            var winHeight = $window.height();
            this._update(winScroll, winHeight);
        },

        _update: function(winScroll, winHeight) {
            if (this.options.disabled) {
                return
            }

            var blockTop = this.element.offset().top;
            var blockHeight = this.element.outerHeight();
            var scrollFrom = blockTop - winHeight;
            var scrollTo = blockTop + blockHeight;
            if ((winScroll < scrollFrom) || (winScroll > scrollTo)) {
                return
            }

            var scrollLength = scrollTo - scrollFrom;
            var scrollPosition = (winScroll - scrollFrom) / scrollLength;
            var eProgress = $.easing[this.options.easing](scrollPosition);

            this._trigger('update', null, {
                widget: this,
                progress: eProgress
            });
        },

        _setOptionDisabled: function(value) {
            this._super(value);
            this._updateEnabled();
        },

        _updateEnabled: function() {
            if (this.options.disabled) {
                this._addClass(this.image, 'parallax-image-disabled');
                this._removeClass(this.image, 'parallax-image-enabled');
            } else {
                this._removeClass(this.image, 'parallax-image-disabled');
                this._addClass(this.image, 'parallax-image-enabled');
                this.update();
            }
        },

        _destroy: function() {
            this.element.css({
                position: '',
                overflow: ''
            });

            this.image.css({
                minHeight: ''
            });

            $.bgInspector.ignore(this.image);
        }
    });


    var updateParallaxes = function() {
        var winScroll = $window.scrollTop();
        var winHeight = $window.height();
        $(':django-parallax').each(function() {
            var widget = $(this).parallax('instance');
            $.animation_frame(function() {
                widget._update(winScroll, winHeight);
            })(widget.image.get(0));
        });
    };

    $window.on('scroll.parallax', updateParallaxes);
    $window.on('load.parallax', updateParallaxes);
    $window.on('resize.parallax', $.rared(updateParallaxes, 100));

})(jQuery);
