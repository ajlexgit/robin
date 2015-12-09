(function($) {

    /*
        Обработчик перетаскивания файлов.

        Требует:
            jquery.utils.js

        Параметры:
            dragOverClass   - класс, который вешается на DOM-элемент
                              при перетаскивании над ним файла

        События:
            start.drag      - начало перетаскивания над областью
            stop.drag       - завершение перетаскивания над областью
            drop.drag       - файлы переместили на область
     */
    window.FileDropper = Class(EventedObject, function Uploader(cls, superclass) {
        cls.prototype.init = function(root, options) {
            superclass.prototype.init.call(this);

            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend({
                dragOverClass: 'dragover'
            }, options);

            var that = this;
            var drag_counter = 0;
            this.$root.on('dragenter.file_dropper', function() {
                drag_counter++;
                if (drag_counter == 1) {
                    $(this).addClass(that.opts.dragOverClass);

                    // callback
                    that.trigger('start.drag');
                }
            }).on('dragover.file_dropper', function() {
                return false;
            }).on('dragleave.file_dropper', function() {
                drag_counter--;
                if (drag_counter === 0) {
                    $(this).removeClass(that.opts.dragOverClass);

                    // callback
                    that.trigger('stop.drag');
                }
            }).on('drop.file_dropper', function(event) {
                drag_counter = 0;
                $(this).removeClass(that.opts.dragOverClass);

                // callback
                that.trigger('stop.drag');

                var files = that.getFiles(event.originalEvent.dataTransfer);
                if (files.length) {
                    that.trigger('drop.drag', files);
                }
            });

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            this.$root.off('.file_dropper');
            this.$root.removeData(cls.dataParamName);
            superclass.prototype.destroy.call(this);
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

})(jQuery);