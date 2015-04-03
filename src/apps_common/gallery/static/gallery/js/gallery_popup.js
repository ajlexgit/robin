(function($) {
    
    var ARROW = 'gallery-button';
    var LEFT_ARROW = 'gallery-left-button';
    var RIGHT_ARROW = 'gallery-right-button';
    var MAIN_IMAGE = 'gallery-image';
    
    var Gallery = function($container, selector) {
        var that = this;
        var popup = $.popup();
        var $current_item;
        
        this.getCurrent = function() {
            return $current_item;
        };
        
        this._setCurrent = function($item) {
            $current_item = $item;
        };
        
        this._nextOf = function($item) {
            // Получение следующего элемента
            var $next = $item.next(selector);
            if ($next.length) {
                return $next;
            } else {
                return $item.parent().find(selector).first();
            }
        };
        
        this._previousOf = function($item) {
            // Получение предыдущего элемента
            var $prev = $item.prev(selector);
            if ($prev.length) {
                return $prev;
            } else {
                return $item.parent().find(selector).last();
            }
        };
        
        this._activate_image = function($item) {
            // Показ элемента $item, если он содержит картинку
            $.imageDeferred(
                $item.data('big')
            ).done(function(img) {
                var $main_img = $('<img>').addClass(MAIN_IMAGE).prop('src', img.src);
                popup.update({
                    classes: 'popup-gallery',
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
                
                popup.$content.css({
                    maxWidth: img.width,
                    maxHeight: img.height
                });
                
                var max_height = popup.$window.height();
                if ($main_img.height() > max_height) {
                    $main_img.width('').height(max_height);
                }
            }).fail(function() {
                $.popup().hide();
            });
        };

        this._activate_video = function($item) {
            // Показ элемента $item, если он содержит видео
            var $frame = $('<div>').attr('id', 'gallery-video-player');
            
            popup.update({
                classes: 'popup-gallery popup-gallery-video',
                content: $frame,
                clean: true,
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
                    popup.on('slide.gallery hide.gallery', function() {
                        if (player.stopVideo) {
                            player.stopVideo();
                        }
                        popup.off('.gallery');
                    });
                })
            } else if (provider == 2) {
                // Vimeo
                $.vimeo($frame, {
                    videoId: $item.data('key')
                }, function(player) {
                    popup.on('slide.gallery hide.gallery', function() {
                        if (player.api) {
                            player.api('pause');
                        }
                        popup.off('.gallery');
                    });
                })
            }
        };
        
        this._activate = function($item) {
            // Показ элемента $item
            this._setCurrent($item);
            if ($item.hasClass('gallery-item-video-link')) {
                this._activate_video($item);
            } else {
                this._activate_image($item);
            }
        };
        
        this.open = function($item) {
            // Открытие окна галереи с активацией элемента $item
            popup = $.popup.force({
                classes: 'preloader',
                ui: $.noop,
                outClick: $.noop
            });
            popup.trigger('open.gallery');
            this._activate($item);
        };
        
        this.slide_right = function() {
            // Переход к следующему элементу галереи
            var $next = that._nextOf(that.getCurrent());
            if (!$next.length) return;
            
            popup.update({
                classes: 'popup-gallery preloader',
                outClick: $.noop
            });
            
            popup.trigger('slide.gallery');
            popup.trigger('slide-right.gallery');
            that._activate($next);
            return false;
        };
        
        this.slide_left = function() {
            // Переход к предыдущему элементу галереи
            var $prev = that._previousOf(that.getCurrent());
            if (!$prev.length) return;
            
            popup.update({
                classes: 'popup-gallery preloader',
                outClick: $.noop
            });
            
            popup.trigger('slide.gallery');
            popup.trigger('slide-left.gallery');
            that._activate($prev);
            return false;
        };
        
        // Сохранение объекта
        $container.data('gallery', this);
        
        // Защита от дублирования событий при повторном создании
        $container.off('.gallery');
        $(window).off('.gallery');
        $(document).off('.gallery');
        
        // Открытие галереи при клике на элемент
        $container.on('click.gallery', selector, function() {
            that.open($(this));
            return false;
        });
        
        // События стрелок
        $(document).on('click.gallery', '.' + LEFT_ARROW, this.slide_left);
        $(document).on('click.gallery', '.' + RIGHT_ARROW, this.slide_right);
        
        // Прокрутка элементов при клике на главной картинке
        $(document).on('click.gallery', '.' + MAIN_IMAGE, $.rared(function(event) {
            that.slide_right();
        }, 100));
        
        // Обновление размеров окна
        $(window).on('resize.gallery', $.rared(function() {
            if (!popup) return;
            
            var $main_img = popup.$content.find('.' + MAIN_IMAGE);
            $main_img.css({
                height: 'auto'
            });
            var img_height = $main_img.height(),
                max_height = popup.$window.height();
            if (img_height > max_height) {
                $main_img.width('').height(max_height);
            }
        }, 100));
    };
    
    
    $.fn.gallery = function() {
        return this.each(function() {
            new Gallery($(this), '.gallery-item');
        })
    }
    
})(jQuery);