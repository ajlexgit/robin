(function($) {

    /*
        Класс, отвечающий за показ модального окна $.dialog() для
        обрезки картинки.

        Требует:
            jquery.utils.js, jquery-ui.js, jquery.Jcrop.js

        Параметры:
            eventTypes              - события, при возникновении которых будет открыто окно.

            buttonSelector          - CSS-селектор выбора элементов, на которых будут
                                      перехватываться события eventTypes. Выборка
                                      распространяется только на дочерние элементы $root.

            dialogImageMaxSize      - Максимальный размер картинки в окне

            dialogOptions           - Дополнительные опции $.dialog()

            getImage                - Функция, которая должна вернуть URL до исходника картинки

            getMinSize, getMaxSize  - Функции, которые могут вернуть массив ограничений размеров
                                      картинки при обрезке в формате [WIDTH, HEIGHT].
                                      Для форматирования строки вида "120x100" можно использовать
                                      функцию this.formatSize()

            getAspects              - Функция, которая может вернуть отношения ширины к высоте
                                      картинки при обрезке.
                                      Для форматирования строки вида "aspect1|aspect2" можно
                                      использовать функцию this.formatAspects()

            getCropCoords           - Функция, которая может вернуть координаты начального положения
                                      области обрезки в формате массива [LEFT, TOP, WIDTH, HEIGHT].
                                      Для форматирования строки вида "50:50:100:100" можно
                                      использовать функцию this.formatCoords()

            beforeOpen              - Функция, вызываемая перед открытием окна. Если вернёт false,
                                      окно не будет открыто.

            onCrop                  - Функция, вызываемая после того, как область обрезки выбрана.
                                      Аргумент coords - массив [LEFT, TOP, WIDTH, HEIGHT]

            onCancel                - Функция, вызываемая при отмене изменений области обрезки.

        Пример:
            CropDialog.create('.gallery', {
                eventTypes: 'click',
                buttonSelector: 'button.crop'
            })
     */
    window.CropDialog = Class(null, function(cls, superclass) {
        cls.init = function(root, options) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.warn('CropDialog can\'t find root element');
                return false;
            } else {
                this.$root.data('cropdialog', this);
            }

            // настройки
            this.opts = $.extend(true, this.getDefaultOpts(), options);

            var that = this;

            // открытие окна при наступлении событий eventTypes
            this.$root.on(this.opts.eventTypes, this.opts.buttonSelector, function() {
                return that.eventHandler($(this));
            });
        };

        /*
            Настройки по умолчанию
         */
        cls.prototype.getDefaultOpts = function() {
            return {
                eventTypes: 'click',
                buttonSelector: 'button',
                dialogImageMaxSize: [600, 500],
                dialogOptions: {},

                beforeOpen: function($button) {

                },

                getImage: function($button) {

                },
                getMinSize: function($button) {

                },
                getMaxSize: function($button) {

                },
                getAspects: function($button) {

                },
                getCropCoords: function($button) {

                },

                onCrop: function($button, coords) {
                    $button.data('crop-coords', coords.join(':'));
                },
                onCancel: function($butoon, coords) {

                }
            }
        };

        /*
            Форматирует строку вида '120x120' в массив [120, 120].
            Если строка некорректна, вернет undefined
         */
        cls.prototype.formatSize = function(value) {
            var arr = [];

            if ($.isArray(value)) {
                arr = value
            } else if (typeof value == 'string') {
                arr = value.split('x');
            } else if (!value) {
                return
            } else {
                arr = value.toString().split('x');
            }

            arr = arr.map(function(item) {
                var num = Number(item);
                return num && num.toFixed(0);
            }).filter($.isNumeric).slice(0, 2);

            if (arr.length == 2) {
                return arr
            }
        };

        /*
            Форматирует строку аспектов вида '1.5|1.66' в массив [1.5, 1.66].
            Если строка некорректна, вернет undefined
         */
        cls.prototype.formatAspects = function(value) {
            var arr = [];

            if ($.isArray(value)) {
                arr = value
            } else if (typeof value == 'string') {
                arr = value.split('|');
            } else if (!value) {
                return
            } else {
                arr = value.toString().split('|');
            }

            arr = arr.map(function(item) {
                return parseFloat(item);
            }).filter($.isNumeric).slice(0, 2);

            if (arr.length) {
                return arr
            }
        };

        /*
            Форматирует строку вида '50:50:150:150' в массив [50, 50, 150, 150].
            Если строка некорректна, вернет undefined
         */
        cls.prototype.formatCoords = function(value) {
            var arr = [];

            if ($.isArray(value)) {
                arr = value
            } else if (typeof value == 'string') {
                arr = value.split(':');
            } else if (!value) {
                return
            } else {
                arr = value.toString().split(':');
            }

            arr = arr.map(function(item) {
                var num = Number(item);
                return num && num.toFixed(0);
            }).filter($.isNumeric).slice(0, 4);

            if (arr.length == 4) {
                return arr
            }
        };

        /*
            Обработчик целевого события eventTypes на кнопке
         */
        cls.prototype.eventHandler = function($button) {
            // callback
            if (this.opts.beforeOpen.call(this, $button) === false) {
                return false;
            }

            // настройки обрезки
            var crop_opts = this.collectCropOptions($button);
            if (!crop_opts) {
                console.warn('CropDialog can\'t collect crop options');
                return false
            }

            var dialog_opts = this.collectDialogOptions($button, crop_opts);
            this.openDialog(dialog_opts, crop_opts);

            return false;
        };

        /*
            Получение настроек обрезки.
            Если настройки некорректны, должен вернуть false
         */
        cls.prototype.collectCropOptions = function($button) {
            var options = {};

            var image = this.opts.getImage.call(this, $button);
            if (!image) {
                console.warn('CropDialog can\'t find image url');
                return false
            }

            options.image = image;
            options.min_size = this.opts.getMinSize.call(this, $button);
            options.max_size = this.opts.getMaxSize.call(this, $button);
            options.aspects = this.opts.getAspects.call(this, $button);
            options.cropcoords = this.opts.getCropCoords.call(this, $button);

            return options;
        };

        /*
            Получение настроек диалогового окна
         */
        cls.prototype.collectDialogOptions = function($button, crop_opts) {
            var that = this;
            return $.extend(true, {
                title: gettext('Crop image'),
                width: 610,
                minHeight: 300,
                closeText: '',
                show: {
                    effect: "fadeIn",
                    duration: 100
                },
                hide: {
                    effect: "fadeOut",
                    duration: 100
                },
                modal: true,
                resizable: false,
                position: {
                    my: "center top",
                    at: "center top+40",
                    of: window
                },
                buttons: [
                    {
                        text: gettext('Cancel'),
                        click: function() {
                            var coords = that.getCropCoords();
                            that.closeDialog();
                            that.cropCancelled($button, coords);
                        }
                    },
                    {
                        text: gettext('Ok'),
                        click: function() {
                            var coords = that.getCropCoords();
                            that.closeDialog();
                            that.applyCrop($button, coords);
                        }
                    }
                ],
                open: function() {
                    that.onDialogOpened(crop_opts);
                },
                close: function() {
                    that.onDialogClosed(crop_opts);
                }
            }, this.opts.dialogOptions);
        };

        /*
            Создание и открытие модального окна
         */
        cls.prototype.openDialog = function(dialog_opts, crop_opts) {
            var $template = $('<div/>').addClass('preload').appendTo('body');
            this.$dialog = $template.dialog(dialog_opts);
        };

        /*
            Инициализация плагина обрезки
         */
        cls.prototype.initJCrop = function($image, crop_opts) {
            // отношение реальных размеров картинки к размерам картинки в окне
            this.preview_relation_x = $image.prop('naturalWidth') / $image.width();
            this.preview_relation_y = $image.prop('naturalHeight') / $image.height();

            var that = this;

            // Инициализация jCrop
            $image.Jcrop({
                keySupport: false,
                bgOpacity: 0.3,
                boxWidth: that.opts.dialogImageMaxSize[0],
                boxHeight: that.opts.dialogImageMaxSize[1],
                boundary: 0
            }, function() {
                that.jcrop_api = this;

                // Ограничения размеров
                if (crop_opts.min_size) {
                    var minSize = [
                        Math.ceil(crop_opts.min_size[0] / that.preview_relation_x),
                        Math.ceil(crop_opts.min_size[1] / that.preview_relation_y)
                    ];
                    that.jcrop_api.setOptions({minSize: minSize});
                    that.jcrop_api.setSelect([0, 0].concat(minSize));
                }
                if (crop_opts.max_size) {
                    var maxSize = [
                        Math.floor(crop_opts.max_size[0] / that.preview_relation_x),
                        Math.floor(crop_opts.max_size[1] / that.preview_relation_y)
                    ];
                    that.jcrop_api.setOptions({maxSize: maxSize})
                }

                // Аспекты
                if (crop_opts.aspects) {
                    that.jcrop_api.setOptions({aspectRatio: crop_opts.aspects[0]});
                }

                // Положение кропа
                if (crop_opts.cropcoords) {
                    var preview_crop_x = crop_opts.cropcoords[0] / that.preview_relation_x;
                    var preview_crop_y = crop_opts.cropcoords[1] / that.preview_relation_y;
                    var preview_crop_w = crop_opts.cropcoords[2] / that.preview_relation_x;
                    var preview_crop_h = crop_opts.cropcoords[3] / that.preview_relation_y;

                    that.jcrop_api.setOptions({
                        setSelect: [
                            preview_crop_x,
                            preview_crop_y,
                            preview_crop_x + preview_crop_w,
                            preview_crop_y + preview_crop_h
                        ]
                    });
                }
            });
        };

        /*
            Рассчет области обрезки в окне, с учетом уменьшенного масштаба картинки
         */
        cls.prototype.getCropCoords = function() {
            var coords = this.jcrop_api.tellSelect();

            // рассчет области обрезки с учетом уменьшения картинки в окне
            return [
                Math.round(this.preview_relation_x * coords.x),
                Math.round(this.preview_relation_y * coords.y),
                Math.round(this.preview_relation_x * coords.w),
                Math.round(this.preview_relation_y * coords.h)
            ];
        };

        /*
            Событие, возникающее когда диалоговое окно открылось
         */
        cls.prototype.onDialogOpened = function(crop_opts) {
            var that = this;

            // загрузка картинки
            $.loadImageDeferred(crop_opts.image).always(function() {
                that.$dialog.removeClass('preload');
            }).done(function(img) {
                var $image = $('<img>').attr({
                    src: img.src
                });

                // добавление картинки в окно
                that.$dialog.prepend($image);

                // инициализация JCrop
                that.initJCrop($image, crop_opts);
            }).fail(function() {
                that.closeDialog();
            });
        };

        /*
            Закрытие окна
         */
        cls.prototype.closeDialog = function() {
            if (this.$dialog && this.$dialog.length) {
                this.$dialog.dialog('close');
            }
        };

        /*
            Событие, возникающее при закрытии окна
         */
        cls.prototype.onDialogClosed = function(crop_opts) {
            if (this.jcrop_api) {
                this.jcrop_api.destroy();
                this.jcrop_api = null;
            }

            if (this.$dialog && this.$dialog.length) {
                this.$dialog.empty();
                this.$dialog.remove();
                this.$dialog = null;
            }
        };

        /*
            Событие, возникающее при отмене обрезки
         */
        cls.prototype.cropCancelled = function($button, coords) {
            this.opts.onCancel.call(this, $button, coords);
        };

        /*
            Событие применения обрезки
         */
        cls.prototype.applyCrop = function($button, coords) {
            this.opts.onCrop.call(this, $button, coords);
        };
    });

})(jQuery);
