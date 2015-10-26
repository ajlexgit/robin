(function($) {

    window.StdImage = (function() {
        var StdImage = function() {};

        StdImage.create = function(root, options) {
            var self = new StdImage();

            self.$root = $.findFirstElement(root);
            if (!self.$root.length) {
                console.log('StdImage can\'t find root element');
                return
            }

            self.$input = $.findFirstElement('input[type="file"]', self.$root);
            if (!self.$input.length) {
                console.log('StdImage can\'t find file element');
                return
            }

            self.opts = $.extend(self.getDefaultOpts(), options);

            // превью
            self.$previews = $.findFirstElement(self.opts.previewsSelector, self.$root);
            self.$old_preview = $.findFirstElement(self.opts.oldPreviewSelector, self.$root);
            self.$new_preview = $.findFirstElement(self.opts.newPreviewSelector, self.$root);

            self._wasEmpty = self.$root.hasClass(self.opts.emptyClass) || !self.$old_preview.length;

            // EVENTS
            var drag_counter = 0;
            self.$root.off('.stdimage').on('dragenter.stdimage', function() {
                drag_counter++;
                if (drag_counter == 1) {
                    $(this).addClass(self.opts.dragOverClass);
                }
                return false;
            }).on('dragleave.stdimage', function() {
                drag_counter--;
                if (drag_counter === 0) {
                    $(this).removeClass(self.opts.dragOverClass);
                }
                return false;
            }).on('drop.stdimage', function() {
                drag_counter = 0;
                var $this = $(this);
                setTimeout(function() {
                    $this.removeClass(self.opts.dragOverClass);
                }, 0);
            });

            // Изменение файла
            self.$input.off('.stdimage').on('change.stdimage', function() {
                var $input = $(this);

                var file = $input.prop('files');
                file = file && file.length && file[0];
                if (!file) {
                    self.reset();
                    return;
                }

                self.$root.addClass(self.opts.preloaderClass);

                $.fileReaderDeferred(file).done(function(src) {
                    $.loadImageDeferred(src).done(function(img) {
                        src = null;

                        // размер превью
                        var size = self.$root.data('size').toString()
                            .split('x').map(function(item) {
                                return parseInt(item)
                            }).filter(Boolean);
                        if (size.length != 2) {
                            size = [self.$previews.width(), self.$previews.height()];
                        }

                        var final_canvas = $.previewCanvas({
                            source: img,
                            width: size[0],
                            height: size[1],
                            crop: true,
                            stretch: false
                        });


                        self.$root.removeClass(self.opts.emptyClass);
                        self.$root.removeClass(self.opts.preloaderClass);

                        self.$old_preview.hide();
                        self.$new_preview.attr('src', final_canvas.toDataURL()).show();
                    }).fail(function() {
                        self.reset();
                        self.$root.removeClass(self.opts.preloaderClass);
                    })
                }).fail(function() {
                    self.reset();
                    self.$root.removeClass(self.opts.preloaderClass);
                });
            });

            self.$root.data('stdimage', self);

            return self;
        };

        /*
            Настройки по умолчанию
         */
        StdImage.prototype.getDefaultOpts = function() {
            return {
                previewsSelector: '.previews',
                oldPreviewSelector: '.old-preview',
                newPreviewSelector: '.new-preview',

                emptyClass: 'empty',
                dragOverClass: 'dragover',
                preloaderClass: 'preloader'
            }
        };

        /*
            Сброс на первоначальное превью, если оно было
         */
        StdImage.prototype.reset = function() {
            this.$new_preview.removeAttr('src').hide();
            if (this._wasEmpty) {
                this.$root.addClass(this.opts.emptyClass);
            } else {
                this.$old_preview.show();
            }
        };

        return StdImage;
    })();


    $(document).ready(function() {
        $('.stdimage').each(function() {
            StdImage.create(this);
        })
    })

})(jQuery);