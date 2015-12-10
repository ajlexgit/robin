(function($) {

    /*
        Загрузчик файлов. Обертка над Pluploader.

        Требует:
            jquery.utils.js
            plupload.full.min.js

        Параметры:
            url                 - адрес, на который отправляются файлы

            buttonSelector      - CSS-селектор кнопок, открывающих диалоговое окно выбора файла.
                                  Выборка происходит по дочерним элементам $root

            dropSelector        - CSS-селектор области, на которую можно перетаскивать файлы.
                                  Выборка происходит по дочерним элементам $root. Если равен
                                  строке "self" - областью станет сам $root-элемент

            multiple            - можно ли выбирать несколько файлов за раз

            fileName            - имя поля, в котором отправляется файл

            resize              - объект, отвечающий за ресайз на клиенте

            max_size            - строка или число, являющеся ограничением на вес загружаемого файла

            zIndex              - z-index элемента загрузки файла

            onInit              - Событие инициализации загрузчика

            getExtraData        - Функция, возвращающая словарь дополнительных данных,
                                  отправляемых на сервер.

            onFileAdded         - Событие добавления файла в очередь загрузки

            onBeforeFileUpload  - Событие, возникающее перед началом загрузки файла

            onFileUploadProgress - Событие, возникающее в процессе закачки файла

            onFileUploaded      - Событие окончания загрузки файла

            onFileRemoved       - Событие удаления файла из очереди загрузки

            onUploadComplete    - Событие окончания загрузки всех файлов

            onFileUploadError   - Событие ошибки загрузки файла

        Пример:
            Uploader('#root', {
                url: '/upload/',
                buttonSelector: '.button',
                multiple: false,
                resize: {
                    width: 1024,
                    height: 1024
                },
                max_size: '12mb',

                onInit:                 function() {},
                getExtraData:           function() {},
                onFileAdded:            function(file) {},
                onBeforeFileUpload:     function(file) {},
                onFileUploadProgress:   function(file, percent) {},
                onFileUploaded:         function(file, json_response) {},
                onFileRemoved:          function(file) {},
                onUploadComplete:       function(files) {},
                onFileUploadError:      function(file, error, json_response) {},
            });
     */
    window.Uploader = Class(null, function Uploader(cls, superclass) {
        cls.prototype.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            // настройки
            this.opts = $.extend(true, this.getDefaultOpts(), options);

            // инициализация загрузчика
            this.initPluploader();

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return {
                url: '',
                buttonSelector: '',
                dropSelector: '',
                multiple: true,
                fileName: 'image',
                resize: {},
                max_size: 0,
                zIndex: 1,

                onInit: $.noop,
                getExtraData: $.noop,
                onFileAdded: $.noop,
                onBeforeFileUpload: $.noop,
                onFileUploadProgress: $.noop,
                onFileUploaded: $.noop,
                onFileRemoved: $.noop,
                onUploadComplete: $.noop,
                onFileUploadError: $.noop
            }
        };

        /*
            Инициализация загрузчика
         */
        cls.prototype.initPluploader = function() {
            var that = this;
            var config = {
                url: this.opts.url,
                chunk_size: '256kb',
                file_data_name: this.opts.fileName,
                runtimes: 'html5,flash,silverlight,html4',
                flash_swf_url: '/static/common/js/plupload/Moxie.swf',
                silverlight_xap_url: '/static/common/js/plupload/Moxie.xap',
                prevent_duplicates: true,
                multi_selection: this.opts.multiple,
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
                        that._fixZIndex();
                    },
                    Refresh: function() {
                        that._fixZIndex();
                    },
                    FilesAdded: function(up, files) {
                        that.FilesAddedHandler(files);
                    },
                    BeforeUpload: function(up, file) {
                        that.BeforeUploadHandler(file);
                    },
                    UploadProgress: function(up, file) {
                        that.UploadProgressHandler(file);
                    },
                    FileUploaded: function(up, file, response) {
                        that.FileUploadedHandler(file, response);
                    },
                    FilesRemoved: function(up, files) {
                        that.FilesRemovedHandler(files);
                    },
                    UploadComplete: function(up, files) {
                        that.UploadCompleteHandler(files);
                    },
                    Error: function(up, error) {
                        that.ErrorHandler(error);
                    }
                }
            };

            // кнопка загрузки
            if (this.opts.buttonSelector) {
                if (typeof this.opts.buttonSelector == 'string') {
                    config['browse_button'] = this.$root.find(this.opts.buttonSelector).get(0);
                } else if (this.opts.buttonSelector.jquery) {
                    config['browse_button'] = this.opts.buttonSelector.get(0);
                } else {
                    config['browse_button'] = this.opts.buttonSelector;
                }
            }

            // область перетаскивания файлов
            if (this.opts.dropSelector) {
                if (this.opts.dropSelector == 'self') {
                    this.$drop = this.$root;
                } else {
                    this.$drop = this.$root.find(this.opts.dropSelector).first();
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
            Событие инициализации загрузчика
         */
        cls.prototype.InitHandler = function() {
            // добавление класса на $root при перетаскивании файлов
            this._initFileDrop();

            this.opts.onInit.call(this);

            // установка дополнительных данных загрузки
            var extra_data = this.opts.getExtraData.call(this);
            if (extra_data) {
                this.uploader.setOption('multipart_params', extra_data);
            }
        };

        /*
            Добавление класса на $root при перетаскивании файлов
         */
        cls.prototype._initFileDrop = function() {
            if (!this.uploader.features.dragdrop) {
                return
            }

            var that = this;
            var drag_counter = 0;
            this.$drop.off('.uploader')
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
        };

        /*
            Добавление z-index из-за косяка в режиме мобильной версии
         */
        cls.prototype._fixZIndex = function() {
            this.$root.find('.moxie-shim').css({
                zIndex: this.opts.zIndex
            }).find('input').css({
                zIndex: this.opts.zIndex,
                cursor: 'pointer'
            });
        };

        /*
            Освобождение ресурсов
         */
        cls.prototype.destroy = function() {
            if (this.uploader) {
                this.uploader.destroy();
                this.uploader = null;
            }

            if (this.$drop && this.$drop.length) {
                this.$drop.off('.uploader');
            }

            this.$root.removeData(cls.dataParamName);
        };

        /*
            Удаление файла из очереди
         */
        cls.prototype.removeFile = function(file_id) {
            if (this.uploader && file_id) {
                this.uploader.removeFile(file_id);
            }
        };

        /*
            Событие добавления файлов в очередь
         */
        cls.prototype.FilesAddedHandler = function(files) {
            var that = this;

            plupload.each(files, function(file) {
                that.opts.onFileAdded.call(that, file);
            });

            // начинать загрузку сразу
            this.uploader.start();
        };

        /*
            Событие перед началом загрузки файла
         */
        cls.prototype.BeforeUploadHandler = function(file) {
            this.opts.onBeforeFileUpload.call(this, file);
        };

        /*
            Событие прогресса закачки файла
         */
        cls.prototype.UploadProgressHandler = function(file) {
            this.opts.onFileUploadProgress.call(this, file, file.percent);
        };

        /*
            Cобытие успешной загрузки файла.
            Ожидает ответ в формате JSON.
         */
        cls.prototype.FileUploadedHandler = function(file, response) {
            var json_response = $.parseJSON(response.response);
            this.opts.onFileUploaded.call(this, file, json_response);
        };

        /*
            Событие удаления файлов из очереди
         */
        cls.prototype.FilesRemovedHandler = function(files) {
            var that = this;

            plupload.each(files, function(file) {
                that.opts.onFileRemoved.call(that, file);
            });
        };

        /*
            Событие успешной загрузки всех файлов.
         */
        cls.prototype.UploadCompleteHandler = function(files) {
            this.opts.onUploadComplete.call(this, files);
        };

        /*
            Событие ошибки загрузки файла.
            Ожидает ответ в формате JSON.
         */
        cls.prototype.ErrorHandler = function(error) {
            var json_response = error.response && $.parseJSON(error.response);
            var short_error = {
                code: error.code,
                message: error.message,
                status: error.status
            };
            this.opts.onFileUploadError.call(this, error.file, short_error, json_response);
        };
    });
    Uploader.dataParamName = 'uploader';

})(jQuery);