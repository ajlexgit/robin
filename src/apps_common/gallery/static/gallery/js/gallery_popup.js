(function($) {

    /*
        Стандартная галерея, показывающая фото и видео на весь экран
        в модальном окне.

        Требует:
            jquery.utils.js,
            jquery.popups.js,
            slider.js,
            jquery.youtube.js,
            jquery.vimeo.js

        Параметры:
            previews: str / jquery       - превью-элементы галереи
            activePreview: DOM / index   - DOM-элемент или индекс начальной картинки


        У превью-элементов картинок обязателен атрибут data-src.
        Опционально, можно указать атрибуты data-srcset и data-sizes.

        У превью-элементов видео обязательны атрибуты data-src, data-provider и data-key.
        Поддерживаются только провайдеры "youtube" и "vimeo".
        Опционально, можно указать атрибуты data-srcset и data-sizes.


        Пример HTML:
            <div id="gallery">
                <div class="item" data-src="...">
                    <img src="...">
                </div>

                <div class="item" data-src="..." data-provider="youtube" data-key="...">
                    <img src="...">
                </div>

                ...
            </div>



            $('#gallery').find('.item').on('click', function() {
                $.gallery({
                    previews: '#gallery .item',
                    activePreview: this
                });
            });

     */

    window.GalleryPopup = Class(OverlayedPopup, function GalleryPopup(cls, superclass) {
        cls.defaults = $.extend({}, superclass.defaults, {
            imageItemClass: 'image-item',
            videoItemClass: 'video-item',
            videoPlayingClass: 'playing',

            previews: '',
            activePreview: 0
        });

        cls.OVERLAY_ID = 'gallery-popup-overlay';
        cls.CONTAINER_ID = 'gallery-popup-container';

        cls.init = function(options) {
            superclass.init.call(this, options);

            this.$previews = this.opts.previews;
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
            var $image;
            var preview_data = $preview.data();

            // картинка (для всех типов)
            if (preview_data.src) {
                // картинка
                $image = $('<img>').attr('src', preview_data.src);

                // атрибуты srcset и sizes
                if (preview_data.srcset) {
                    $image.attr({
                        srcset: preview_data.srcset,
                        sizes: preview_data.sizes || '100vw'
                    })
                }
            }

            // проверка наличия картинки
            if (!$image || ($image.length != 1)) {
                return
            }

            if (preview_data.provider && preview_data.key) {
                // видео
                var $video = $('<div/>').addClass(this.opts.videoItemClass);
                $video.append($image);

                // кнопка воспроизведения
                var $playBtn = $('<div/>').addClass('play-btn');
                $video.append($playBtn);

                var that = this;
                $playBtn.on(touchClick, function() {
                    that.playVideo($(this).closest('.' + that.opts.videoItemClass));
                });

                $video.data({
                    provider: preview_data.provider,
                    key: preview_data.key
                });
                return $video;
            } else {
                // картинка
                return $image.addClass(this.opts.imageItemClass);
            }
        };

        /*
            Содержимое окна
         */
        cls.resetContent = function() {
            var that = this;
            var $items = this.$previews.map(function(i, preview) {
                var $preview = $(preview);
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
            Создание объекта слайдера
         */
        cls.makeSlider = function() {
            return Slider(this.$content.find('.slider'), {
                sliderHeight: Slider.prototype.HEIGHT_NONE,
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

        /*
            Добавление слайдера
         */
        cls.extraDOM = function() {
            superclass.extraDOM.call(this);

            this.slider = this.makeSlider();
            if (!this.slider) {
                this.error('slider wasn\'t created');
                return;
            }

            // выделение выбранного слайда
            var preview;
            var active_index = 0;
            if (this.opts.activePreview.jquery) {
                // jQuery-селектор с превью-элементом
                preview = this.opts.activePreview.get(0);
                active_index = this.$previews.toArray().indexOf(preview);
            } else if (this.opts.activePreview.nodeType == 1) {
                // DOM-элемент превью-элемента
                preview = this.opts.activePreview;
                active_index = this.$previews.toArray().indexOf(preview);
            } else {
                // индекс активного слайда
                active_index = this.opts.activePreview;
            }

            // проверка индекса
            if ((active_index < 0) || (active_index >= this.slider.$slides.length)) {
                active_index = 0;
                this.warn('active preview not found', this.opts.activePreview);
            }

            var $activeSlide = this.slider.$slides.eq(active_index);
            this.slider.slideTo($activeSlide, 'instant');
        };

        /*
            Уничтожение слайдера
         */
        cls._removeDOM = function() {
            if (this.slider) {
                this.slider.destroy();
                this.slider = null;
            }

            if (this._player) {
                this._player.destroy();
                this._player = null;
            }

            superclass._removeDOM.call(this);
        };

        /*
            Инициализация видеоплеера
         */
        cls.playVideo = function($item) {
            var item_data = $item.data();

            if (this._player) {
                this._player.destroy();
                this._player = null;
            }

            var that = this;
            var $player = $('<div>');
            $item.append($player);
            if (item_data.provider == 'youtube') {
                this._player = YouTube($player, {
                    video: item_data.key,
                    autoplay: true
                }).on('ready', function() {
                    $item.addClass(that.opts.videoPlayingClass);
                });
            } else if (item_data.provider == 'vimeo') {
                this._player = Vimeo($player, {
                    video: item_data.key,
                    autoplay: true
                }).on('ready', function() {
                    $item.addClass(that.opts.videoPlayingClass);
                });
            }

            // остановка видео при переходе на другой слайд и закрытии окна
            if (this._player) {
                this.on('before_hide.video', function() {
                    that.stopVideo($item);
                });

                this.slider.on('before_change.video', function() {
                    that.stopVideo($item);
                });
            }
        };

        /*
            Уничтожение видеоплеера
         */
        cls.stopVideo = function($item) {
            if (this._player) {
                this._player.destroy();
                this._player = null;
            }

            $item.removeClass(this.opts.videoPlayingClass);
            $item.find('iframe').remove();

            this.off('.video');
            if (this.slider) {
                this.slider.off('.video');
            }
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