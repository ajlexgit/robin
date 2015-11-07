(function($) {

    window.StdImage = Class(null, function(cls, superclass) {
        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.log('StdImage can\'t find root element');
                return false;
            }

            this.$input = this.$root.find('input[type="file"]');
            if (!this.$input.length) {
                console.log('StdImage can\'t find file element');
                return false;
            }

            // настройки
            this.opts = $.extend({
                previewsSelector: '.previews',
                oldPreviewSelector: '.old-preview',
                newPreviewSelector: '.new-preview',

                emptyClass: 'empty',
                dragOverClass: 'dragover',
                preloaderClass: 'preloader'
            }, options);

            // превью
            this.$previews = this.$root.find(this.opts.previewsSelector);
            this.$old_preview = this.$root.find(this.opts.oldPreviewSelector);
            this.$new_preview = this.$root.find(this.opts.newPreviewSelector);

            this.$root.data('stdimage', this);

            // значение не установлено изначально
            this._wasEmpty = this.$root.hasClass(this.opts.emptyClass) || !this.$old_preview.length;

            var that = this;
            var drag_counter = 0;

            // вешаем класс на перетаскивании
            this.$root.on('dragenter.stdimage', function() {
                drag_counter++;
                if (drag_counter == 1) {
                    $(this).addClass(that.opts.dragOverClass);
                }
                return false;
            }).on('dragleave.stdimage', function() {
                drag_counter--;
                if (drag_counter === 0) {
                    $(this).removeClass(that.opts.dragOverClass);
                }
                return false;
            }).on('drop.stdimage', function() {
                drag_counter = 0;
                var $this = $(this);
                setTimeout(function() {
                    $this.removeClass(that.opts.dragOverClass);
                }, 0);
            });

            // Изменение файла
            this.$input.on('change.stdimage', function() {
                that.changeHandler($(this));
            });
        };

        /*
            Событие изменения файла
         */
        cls.prototype.changeHandler = function($input) {
            var file = $input.prop('files');
            file = file && file.length && file[0];
            if (!file) {
                this.reset();
                return;
            }

            this.$root.addClass(this.opts.preloaderClass);

            var that = this;
            $.fileReaderDeferred(file).done(function(src) {
                $.loadImageDeferred(src).done(function(img) {
                    src = null;

                    // размер превью
                    var size = that.$root.data('size').toString()
                        .split('x').map(function(item) {
                            return parseInt(item)
                        }).filter(Boolean);
                    if (size.length != 2) {
                        size = [that.$previews.width(), that.$previews.height()];
                    }

                    // создаем превью
                    var final_canvas = $.previewCanvas({
                        source: img,
                        width: size[0],
                        height: size[1],
                        crop: true,
                        stretch: false
                    });

                    that.$root.removeClass(that.opts.emptyClass);
                    that.$root.removeClass(that.opts.preloaderClass);

                    that.$old_preview.hide();
                    that.$new_preview.attr('src', final_canvas.toDataURL()).show();
                }).fail(function() {
                    that.reset();
                    that.$root.removeClass(that.opts.preloaderClass);
                })
            }).fail(function() {
                that.reset();
                that.$root.removeClass(that.opts.preloaderClass);
            });
        };

        /*
            Сброс на первоначальное превью, если оно было
         */
        cls.prototype.reset = function() {
            this.$new_preview.removeAttr('src').hide();
            if (this._wasEmpty) {
                this.$root.addClass(this.opts.emptyClass);
            } else {
                this.$old_preview.show();
            }
        };
    });


    $(document).ready(function() {
        $('.stdimage').each(function() {
            StdImage.create(this);
        })
    })

})(jQuery);