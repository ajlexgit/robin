(function($) {

    /*
        Стандартная галерея, показывающая фото и видео на весь экран
        в модальном окне.

        Требует:
            jquery.utils.js, jquery.popups.js, slider.js

        Параметры:
            previews: str / jquery       - превью-элементы галереи


        У превью-элементов картинок обязателен атрибут data-src.
        Опционально, можно указать атрибуты data-srcset и data-sizes.

        У превью-элементов видео обязательны атрибуты data-provider и data-key.
        Поддерживаются только провайдеры "youtube" и "vimeo".
     */

    var GallerySlider = Class(Slider, function GallerySlider(cls, superclass) {
        cls.calcListHeight = function() {

        }
    });



    window.GalleryPopup = Class(OverlayedPopup, function GalleryPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            previews: ''
        });

        cls.OVERLAY_ID = 'gallery-popup-overlay';
        cls.CONTAINER_ID = 'gallery-popup-container';

        cls.init = function(options) {
            superclass.init.call(this, options);

            this.$previews = this.opts.items;
            if (!this.$previews) {
                return this.raise('previews required');
            }
            if (typeof this.$previews == 'string') {
                // получаем jquery, в случае селектора
                this.$previews = $(this.$previews);
            }
            if (!this.$previews.jquery || !this.$previews.length) {
                return this.raise('previews not found');
            }
        };

        /*
            Создание элемента окна галереи из элемента превью
         */
        cls._buildItem = function($preview) {
            var preview_data = $preview.data();

            if (preview_data.src) {
                // картинка
                var $item = $('<img>').attr('src', preview_data.src);

                // атрибуты srcset и sizes
                if (preview_data.srcset) {
                    $item.attr({
                        srcset: preview_data.srcset,
                        sizes: preview_data.sizes || '100vw'
                    })
                }

                return $item;
            } else if (preview_data.provider && preview_data.key) {
                // видео
            }
        };

        /*
            Содержимое окна
         */
        cls.resetContent = function() {
            var that = this;
            var $items = this.$previews.map(function(i, preview) {
                var $preview = $(preview);

                // создание элемента галереи
                var $item = that._buildItem($preview);

                if (!$item || !$item.length) {
                    that.warn('not builded item from preview ', $preview);
                    return;
                }

                if ($item.length > 1) {
                    that.warn('item contains more that one element ', $preview);
                    return;
                }

                return $item.get(0);
            });

            // хоть один элемент галереи должен быть
            if (!$items.length) {
                return this.raise('at least one gallery item required');
            }

            // слайдер
            var $slider = $('<div>').addClass('slider no-slider').append(
                $items.addClass('slider-item')
            );

            this.$content.html($slider);
        };

        /*
            Дополнительные элементы
         */
        cls.extraDOM = function() {
            superclass.extraDOM.call(this);

            this.slider = GallerySlider(this.$content.find('.slider'), {
                itemSelector: '.slider-item'
            }).attachPlugins([
                SliderSideAnimation({}),
                SliderSideShortestAnimation({}),
                SliderControlsPlugin({
                    animationName: 'side-shortest'
                }),
                SliderNavigationPlugin({
                    animationName: 'side'
                }),
                SliderDragPlugin({
                    slideMarginPercent: 2
                })
            ])
        };
    });


    $.gallery = function(options) {
        var opts = $.extend({
            classes: 'gallery-popup',
            hideOnClick: false
        }, options);

        var popup = GalleryPopup(opts);
        return popup && popup.show();
    };

})(jQuery);