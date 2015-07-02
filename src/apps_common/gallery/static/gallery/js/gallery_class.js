(function($) {

    var ARROW = 'gallery-button';
    var LEFT_ARROW = 'gallery-left-button';
    var RIGHT_ARROW = 'gallery-right-button';
    var MAIN_IMAGE = 'gallery-image';

    window.Gallery = (function() {
        function Gallery($root, options) {
            this.$root = $root;
            this.settings = $.extend({
                itemSelector: 'img',
                itemVideoClass: 'gallery-item-video-link',
                popupClass: 'popup-gallery',
                popupVideoClass: 'popup-gallery-video'
            }, options);


            var that = this;

            // Открытие галереи при клике на элемент
            this.$root.on('click.gallery', this.settings.itemSelector, function() {
                that.showItem($(this));
                return false;
            });

            // События стрелок окна и клиик на главной картинке
            $(document).on('click.gallery', '.' + LEFT_ARROW, function() {
                that.gotoNext();
            }).on('click.gallery', '.' + RIGHT_ARROW, function() {
                that.gotoPrev();
            }).on('click.gallery', '.' + MAIN_IMAGE, $.rared(function() {
                that.gotoNext();
            }, 100));

            // Обновление размеров окна
            $(window).on('resize.gallery', $.rared(function() {
                if ((!that.popup) || (that.popup != $.popup())) return;

                var $main_img = that.popup.$content.find('.' + MAIN_IMAGE);
                $main_img.css({
                    height: 'auto'
                });
                var img_height = $main_img.height(),
                    max_height = that.popup.$window.height();
                if (img_height > max_height) {
                    $main_img.width('').height(max_height);
                }
            }, 100));

            // Сохранение объекта
            this.$root.data('gallery', this);
        }

        // Получение текущего слайда
        Gallery.prototype.getCurrent = function() {
            return this._current_item;
        };

        // Получение следующего слайда
        Gallery.prototype.nextItem = function($item) {
            var $next = $item.next(this.settings.itemSelector);
            if ($next.length) {
                return $next;
            } else {
                return $item.parent().find(this.settings.itemSelector).first();
            }
        };

        // Получение предыдущего слайда
        Gallery.prototype.prevItem = function($item) {
            var $prev = $item.prev(this.settings.itemSelector);
            if ($prev.length) {
                return $prev;
            } else {
                return $item.parent().find(this.settings.itemSelector).last();
            }
        };

        // Переключение на указанный слайд-картинку
        Gallery.prototype._gotoImageItem = function($item) {
            var that = this;
            $.imageDeferred(
                $item.data('big')
            ).done(function(img) {
                var $main_img = $('<img>').addClass(MAIN_IMAGE).prop('src', img.src);
                that.popup.update({
                    classes: that.settings.popupClass,
                    content: $main_img,
                    clean: false,
                    ui: function(internal) {
                        return [
                            internal.call(this),
                            $('<div>').addClass(ARROW).addClass(LEFT_ARROW),
                            $('<div>').addClass(ARROW).addClass(RIGHT_ARROW)
                        ]
                    },
                    outClick: function() {
                        this.hide();
                    }
                });

                that.popup.$content.css({
                    maxWidth: img.width,
                    maxHeight: img.height
                });

                $main_img.css({
                    height: 'auto'
                });
                var img_height = $main_img.height(),
                    max_height = that.popup.$window.height();
                if (img_height > max_height) {
                    $main_img.width('').height(max_height);
                }
            }).fail(function() {
                that.popup.hide();
            });
        };

        // Переключение на указанный слайд-видео
        Gallery.prototype._gotoVideoItem = function($item) {
            var that = this;
            var $frame = $('<div>').attr('id', 'gallery-video-player');

            that.popup.update({
                classes: that.settings.popupClass + ' ' + that.settings.popupVideoClass,
                content: $frame,
                clean: true,
                ui: function(internal) {
                    return [
                        internal.call(this),
                        $('<div>').addClass(ARROW).addClass(LEFT_ARROW),
                        $('<div>').addClass(ARROW).addClass(RIGHT_ARROW)
                    ]
                }, outClick: function() {
                    this.hide();
                }
            });

            var provider = $item.data('provider');
            if (provider == 1) {
                // Youtube
                $.youtube($frame, {
                    videoId: $item.data('key'),
                    playerVars: {
                        controls: 2,
                        rel: 0
                    }
                }, function(player) {
                    that.popup.on('slide.gallery hide.gallery', function() {
                        if (player.stopVideo) {
                            player.stopVideo();
                        }
                        that.popup.off('.gallery');
                    });
                })
            } else if (provider == 2) {
                // Vimeo
                $.vimeo($frame, {
                    videoId: $item.data('key')
                }, function(player) {
                    that.popup.on('slide.gallery hide.gallery', function() {
                        if (player.api) {
                            player.api('pause');
                        }
                        that.popup.off('.gallery');
                    });
                })
            }
        };

        // Переход к слайду
        Gallery.prototype._gotoItem = function($item) {
            if ((!this.popup) || (this.popup != $.popup())) return;

            this._current_item = $item;
            if ($item.hasClass(this.settings.itemVideoClass)) {
                this._gotoVideoItem($item);
            } else {
                this._gotoImageItem($item);
            }
        };

        // Открытие слайда
        Gallery.prototype.showItem = function($item) {
            this.popup = $.popup.force({
                classes: 'preloader',
                ui: $.noop,
                outClick: $.noop
            });
            this.popup.trigger('open.gallery');
            this._gotoItem($item);
        };

        // Показ следующего слайда
        Gallery.prototype.gotoNext = function() {
            if ((!this.popup) || (this.popup != $.popup())) return;

            var $next = this.nextItem(this.getCurrent());
            if (!$next.length) return;

            this.popup.update({
                classes: this.settings.popupClass + ' preloader',
                outClick: $.noop
            });

            this.popup.trigger('slide.gallery');
            this.popup.trigger('slide-right.gallery');
            this._gotoItem($next);
            return false;
        };

        // Показ предыдущего слайда
        Gallery.prototype.gotoPrev = function() {
            if ((!this.popup) || (this.popup != $.popup())) return;

            var $prev = this.prevItem(this.getCurrent());
            if (!$prev.length) return;

            this.popup.update({
                classes: this.settings.popupClass + ' preloader',
                outClick: $.noop
            });

            this.popup.trigger('slide.gallery');
            this.popup.trigger('slide-left.gallery');
            this._gotoItem($prev);
            return false;
        };

        return Gallery;
    })();

})(jQuery);