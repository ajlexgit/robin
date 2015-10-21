(function($) {

    /*
        Загрузчик файлов. Обертка над Pluploader.

        Требует:
            jquery.utils.js
            plupload.full.min.js
     */

    window.Uploader = (function() {
        var Uploader = function(root, options) {};

        Uploader.create = function(root, options) {
            var self = new Uploader();

            self.$root = $.findFirstElement(root);
            if (!self.$root) {
                console.error('Uploader can\'t find root element');
                return
            }

            self.opts = $.extend({
                url: '',
                buttonSelector: '',
                dropSelector: 'self',
                resize: {},
                max_size: 0,

                // инициализация загрузчика
                // func()
                onInit: $.noop,

                // файл добавлен
                // func(file)
                fileAdded: $.noop,

                // перед нчалом загрузки файла
                // func(file)
                beforeUpload: $.noop,

                // процесс загрузки
                // func(file, percent)
                uploadProgress: $.noop,

                // файл загружен
                // func(file, json_response)
                fileUploaded: $.noop,

                // все файлы загружены
                // func(files)
                uploadComplete: $.noop,

                // файл удален из очереди
                // func(file)
                fileRemoved: $.noop,

                // ошибка загрузки файла
                // func(file, error, json_response)
                onError: $.noop
            }, options);


            // инициализация загрузчика
            self.initUploader();

            self.$root.data('uploader', self);

            return self;
        };

        /*
            Инициализация загрузчика
         */
        Uploader.prototype.initUploader = function() {
            var that = this;
            var config = {
                url: this.opts.url,
                chunk_size: '256kb',
                file_data_name: 'image',
                runtimes: 'html5,flash,silverlight,html4',
                flash_swf_url: '/static/js/plupload/Moxie.swf',
                silverlight_xap_url: '/static/js/plupload/Moxie.xap',
                prevent_duplicates: true,
                resize: this.opts.resize,
                filters: {
                    max_file_size: this.opts.max_size,
                    mime_types: [
                        {title: "Image files", extensions: "jpg,jpeg,png,bmp,gif"}
                    ]
                },
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                init: {
                    Init: function() {
                        that.InitHandler();
                    },
                    FilesAdded: function(up, files) {
                        that.FilesAddedHandler(files);
                    },
                    BeforeUpload: function(up, file) {
                        that.BeforeUploadHandler(file);
                    },
                    FilesRemoved: function(up, files) {
                        that.FilesRemovedHandler(files);
                    },
                    UploadProgress: function(up, file) {
                        that.UploadProgressHandler(file);
                    },
                    FileUploaded: function(up, file, response) {
                        that.FileUploadedHandler(file, response);
                    },
                    UploadComplete: function(up, files) {
                        that.UploadCompleteHandler(files);
                    },
                    Error: function(up, error) {
                        that.ErrorHandler(error);
                    }
                }
            };

            if (this.opts.buttonSelector) {
                config['browse_button'] = $.findFirstElement(this.opts.buttonSelector, this.$root).get(0);
            }

            if (this.opts.dropSelector) {
                if (this.opts.dropSelector == 'self') {
                    this.$drop = this.$root;
                } else {
                    this.$drop = $.findFirstElement(this.opts.dropSelector, this.$root);
                }
                config['drop_element'] = this.$drop.get(0);
            }

            // удаляем старый загрузчик и создаем новый
            if (this.uploader) {
                this.uploader.destroy();
            }
            this.uploader = new plupload.Uploader(config);
            this.uploader.init();
        };


        /*
            Обертка над событием инициализации загрузчика
         */
        Uploader.prototype.InitHandler = function() {
            // Настройки Drag & Drop
            if (this.uploader.features.dragdrop) {
                var that = this;
                var drag_counter = 0;
                this.$drop
                    .off('.uploader')
                    .on('dragenter.uploader', function() {
                        drag_counter++;
                        if (drag_counter == 1) {
                            that.$root.addClass('dragover');
                        }
                    }).on('dragleave.uploader', function() {
                        drag_counter--;
                        if (drag_counter === 0) {
                            that.$root.removeClass('dragover');
                        }
                    }).on('drop.uploader', function() {
                        drag_counter = 0;
                        setTimeout(function() {
                            that.$root.removeClass('dragover');
                        }, 0);
                    });
            }

            this.opts.onInit.call(this);
        };

        /*
            Обертка над событием добавления файлов в очередь
         */
        Uploader.prototype.FilesAddedHandler = function(files) {
            this.processFilesAdded(files);

            // начинать загрузку сразу
            this.uploader.start();
        };

        /*
            Обработка добавленных в очередь файлов
         */
        Uploader.prototype.processFilesAdded = function(files) {
            var that = this;
            plupload.each(files, function(file) {
                that.opts.fileAdded.call(that, file);
            });
        };

        /*
            Обертка над событием перед началом загрузки файла
         */
        Uploader.prototype.BeforeUploadHandler = function(file) {
            this.opts.beforeUpload.call(this, file);
        };

        /*
            Обертка над событием удаления файлов из очереди.
         */
        Uploader.prototype.FilesRemovedHandler = function(files) {
            var that = this;
            plupload.each(files, function(file) {
                that.opts.fileRemoved.call(that, file);
            });
        };

        /*
            Обертка над событием прогресса закачки файла
         */
        Uploader.prototype.UploadProgressHandler = function(file) {
            this.opts.uploadProgress.call(this, file, file.percent);
        };

        /*
            Обертка над событием успешной загрузки файла.
            Ожидает ответ в формате JSON.
         */
        Uploader.prototype.FileUploadedHandler = function(file, response) {
            var json_response = JSON.parse(response.response);
            this.opts.fileUploaded.call(this, file, json_response);
        };

        /*
            Обертка над событием успешной загрузки всех файлов.
         */
        Uploader.prototype.UploadCompleteHandler = function(files) {
            this.opts.uploadComplete.call(this, files);
        };

        /*
            Обертка над событием ошибки загрузки файла.
            Ожидает ответ в формате JSON.
         */
        Uploader.prototype.ErrorHandler = function(error) {
            var json_response = error.response && JSON.parse(error.response);
            var short_error = {
                code: error.code,
                message: error.message,
                status: error.status
            };
            this.opts.onError.call(this, error.file, short_error, json_response);
        };

        return Uploader;
    })();

})(jQuery);