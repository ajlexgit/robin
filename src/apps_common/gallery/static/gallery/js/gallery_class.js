(function($) {

    var galleries = [];

    window.Gallery = Class(null, function Gallery(cls, superclass) {
        cls.prototype.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({
                rootClass: 'gallery-root',
                mainImageClass: 'gallery-image',
                arrowClass: 'gallery-button',
                leftArrowClass: 'gallery-left-button',
                rightArrowClass: 'gallery-right-button',

                itemSelector: 'img',
                itemVideoClass: 'gallery-item-video-link',
                popupClass: 'popup-gallery',
                popupVideoClass: 'popup-gallery-video'
            }, options);

            this.$root.addClass(this.opts.rootClass);

            // Открытие галереи при клике на элемент
            var that = this;
            this.$root.on('click.gallery', this.opts.itemSelector, function() {
                that.showItem($(this));
                return false;
            });

            // События стрелок окна и клик на главной картинке
            $(document).on('click.gallery', '.' + this.opts.leftArrowClass, function() {
                that.gotoPrev();
                return false;
            }).on('click.gallery', '.' + this.opts.rightArrowClass, function() {
                that.gotoNext();
                return false;
            }).on('click.gallery', '.' + this.opts.mainImageClass, function() {
                that.gotoNext();
                return false;
            });

            galleries.push(this);
        };

        // Получение текущего слайда
        cls.prototype.getCurrent = function() {
            return this._current_item;
        };

        // Получение следующего слайда
        cls.prototype.nextItem = function($item) {
            var $next = $item.next(this.opts.itemSelector);
            if ($next.length) {
                return $next;
            } else {
                return $item.parent().find(this.opts.itemSelector).first();
            }
        };

        // Получение предыдущего слайда
        cls.prototype.prevItem = function($item) {
            var $prev = $item.prev(this.opts.itemSelector);
            if ($prev.length) {
                return $prev;
            } else {
                return $item.parent().find(this.opts.itemSelector).last();
            }
        };

        // Переключение на указанный слайд-картинку
        cls.prototype._gotoImageItem = function($item) {
            var that = this;
            $.loadImageDeferred($item.data('big')).done(function(img) {
                var $main_img = $('<img>').addClass(that.opts.mainImageClass).prop('src', img.src);
                that.popup.update({
                    classes: that.opts.popupClass,
                    content: $main_img,
                    clean: false,
                    ui: function() {
                        return [
                            this._defaultUI(),
                            $('<div>').addClass(that.opts.arrowClass).addClass(that.opts.leftArrowClass),
                            $('<div>').addClass(that.opts.arrowClass).addClass(that.opts.rightArrowClass)
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
        cls.prototype._gotoVideoItem = function($item) {
            var that = this;
            var $frame = $('<div>').attr('id', 'gallery-video-player');

            that.popup.update({
                classes: that.opts.popupClass + ' ' + that.opts.popupVideoClass,
                content: $frame,
                ui: function() {
                    return [
                        this._defaultUI(),
                        $('<div>').addClass(that.opts.arrowClass).addClass(that.opts.leftArrowClass),
                        $('<div>').addClass(that.opts.arrowClass).addClass(that.opts.rightArrowClass)
                    ]
                },
                outClick: function() {
                    this.hide();
                }
            });

            var provider = $item.data('provider');
            if (provider == 'youtube') {
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
            } else if (provider == 'vimeo') {
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
        cls.prototype._gotoItem = function($item) {
            if ((!this.popup) || (this.popup != $.popup())) return;

            this._current_item = $item;
            if ($item.hasClass(this.opts.itemVideoClass)) {
                this._gotoVideoItem($item);
            } else {
                this._gotoImageItem($item);
            }
        };

        // Открытие слайда
        cls.prototype.showItem = function($item) {
            this.popup = $.popup.force({
                classes: 'preloader',
                ui: false,
                outClick: false
            });
            this.popup.trigger('open.gallery');
            this._gotoItem($item);
        };

        // Показ следующего слайда
        cls.prototype.gotoNext = function() {
            if ((!this.popup) || (this.popup != $.popup())) return;

            var $next = this.nextItem(this.getCurrent());
            if (!$next.length) return;

            this.popup.update({
                classes: this.opts.popupClass + ' preloader',
                outClick: false
            });

            this.popup.trigger('slide.gallery');
            this.popup.trigger('slide-right.gallery');
            this._gotoItem($next);
            return false;
        };

        // Показ предыдущего слайда
        cls.prototype.gotoPrev = function() {
            if ((!this.popup) || (this.popup != $.popup())) return;

            var $prev = this.prevItem(this.getCurrent());
            if (!$prev.length) return;

            this.popup.update({
                classes: this.opts.popupClass + ' preloader',
                outClick: false
            });

            this.popup.trigger('slide.gallery');
            this.popup.trigger('slide-left.gallery');
            this._gotoItem($prev);
            return false;
        };
    });

    // Обновление размеров окна
    $(window).on('resize.gallery', $.rared(function() {
        $.each(galleries, function(i, gallery) {
            if (!gallery.popup) {
                return
            }

            var $main_img = gallery.popup.$content.find('.' + gallery.opts.mainImageClass);
            $main_img.css({
                height: 'auto'
            });

            var img_height = $main_img.height();
            var max_height = gallery.popup.$window.height();
            if (img_height > max_height) {
                $main_img.width('').height(max_height);
            }
        });
    }, 100));

})(jQuery);
