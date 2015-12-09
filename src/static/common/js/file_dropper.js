(function($) {

    /*
        Обработчик перетаскивания файлов.

        Требует:
            jquery.utils.js


     */
    window.FileDropper = Class(null, function Uploader(cls, superclass) {
        cls.prototype.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({
                dragOverClass: 'dragover',

                onStartDrag: $.noop,
                onStopDrag: $.noop,
                onDrop: $.noop
            }, options);

            var that = this;
            var drag_counter = 0;
            this.$root.on('dragenter.file_dropper', function() {
                drag_counter++;
                if (drag_counter == 1) {
                    $(this).addClass(that.opts.dragOverClass);

                    // callback
                    that.opts.onStartDrag.call(that);
                }
                return false;
            }).on('dragover.file_dropper', function() {
                return false;
            }).on('dragleave.file_dropper', function() {
                drag_counter--;
                if (drag_counter === 0) {
                    $(this).removeClass(that.opts.dragOverClass);

                    // callback
                    that.opts.onStopDrag.call(that);
                }
                return false;
            }).on('drop.file_dropper dragdrop.file_dropper', function(event) {
                drag_counter = 0;
                $(this).removeClass(that.opts.dragOverClass);

                // callback
                that.opts.onStopDrag.call(that);

                var files = that.getFiles(event.originalEvent.dataTransfer);
                if (files.length) {
                    that.opts.onDrop.call(that, files);
                }

                return false;
            });

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            this.$root.off('.file_dropper');
            this.$root.removeData(cls.dataParamName);
        };

        /*
            Получение переданных файлов
         */
        cls.prototype.getFiles = function(transfer) {
            if (!transfer) {
                this.warn('no transfer');
                return [];
            }

            var files = transfer.files;
            if (!files.length) {
                this.warn('no files');
                return [];
            }

            return files;
        }
    });
    FileDropper.dataParamName = 'file_dropper';

    /*
        Алиас для FileDropper
     */
    $.fn.fileDropper = function(options) {
        return this.each(function() {
            FileDropper(this, options)
        })
    }

})(jQuery);