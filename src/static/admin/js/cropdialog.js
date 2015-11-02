(function($) {

    /*
        Открытие диалогового окна с картинкой для кропа

        Требует:
            jquery.utils.js, jquery.canvas.js, jquery-ui.js
    */

    /*
        Форматирует строку вида '120x120' в массив [120, 120]
     */
    var toSize = function(value) {
        var arr;

        if ($.isArray(value)) {
            arr = value
        } else if (typeof value == 'string') {
            arr = value.split('x');
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
        Форматирует строку вида '50:50:150:150' в массив [50, 50, 150, 150]
     */
    var toCoords = function(value) {
        var arr;

        if ($.isArray(value)) {
            arr = value
        } else if (typeof value == 'string') {
            arr = value.split(':');
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
        Форматирует строку аспектов вида '1.5|1.66' в массив [1.5, 1.66]
     */
    var formatAspects = function(value) {
        var arr;

        if ($.isArray(value)) {
            arr = value
        } else if (typeof value == 'string') {
            arr = value.split('|');
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


    window.CropDialog = (function() {
        var CropDialog = function() {};

        CropDialog.create = function(root, options) {
            var self = new CropDialog();

            self.$root = $.findFirstElement(root);
            if (!self.$root.length) {
                console.warn('CropDialog can\'t find root element');
                return
            }

            // настройки
            self.opts = $.extend(true, self.getDefaultOpts(), options);

            // EVENTS
            self.$root.on(self.opts.eventType, self.opts.buttonSelector, function() {
                var options = self.collectDialogOptions($(this));
                if (options) {
                    self.openDialog(options);
                }
                return false;
            });

            self.$root.data('cropdialog', self);

            return self;
        };

        /*
            Настройки по умолчанию
         */
        CropDialog.prototype.getDefaultOpts = function() {
            return {
                eventType: 'click',
                buttonSelector: 'button',

                dialog_opts: {},
                dialog_image_max_size: [600, 500],
                getImage: function($button) {

                },
                getMinSize: function($button) {
                    return $button.data('min-size');
                },
                getMaxSize: function($button) {
                    return $button.data('max-size');
                },
                getAspects: function($button) {
                    return $button.data('aspect');
                },
                getCropCoords: function($button) {
                    return $button.data('crop-coords');
                },

                beforeOpen: function($button) {

                },
                onCrop: function($button, coords) {
                    $button.data('crop-coords', coords.join(':'));
                },
                onCancel: function($butoon) {

                }
            }
        };


        /*
            Получение настроек для открытия диалогового окна
         */
        CropDialog.prototype.collectDialogOptions = function($button) {
            var that = this;
            var options = {};

            // callback
            if (this.opts.beforeOpen.call(this, $button) === false) {
                return
            }

            var image = this.opts.getImage.call(this, $button);
            if (!image) {
                console.warn('CropDialog can\'t find image url');
                return
            } else {
                options.image = image;
            }

            options.min_size = toSize(this.opts.getMinSize.call(this, $button));
            options.max_size = toSize(this.opts.getMaxSize.call(this, $button));
            options.aspects = formatAspects(this.opts.getAspects.call(this, $button));
            options.cropcoords = toCoords(this.opts.getCropCoords.call(this, $button));

            // настройки UI-диалога
            options.dialog_opts = $.extend(true, {
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
                            that.cancelCrop($button, options);
                        }
                    },
                    {
                        text: gettext('Ok'),
                        click: function() {
                            that.applyCrop($button, options);
                        }
                    }
                ],
                open: function() {
                    that.onDialogOpen($button, options);
                },
                close: function() {
                    that.onDialogClose($button, options);
                }
            }, this.opts.dialog_opts);

            return options;
        };


        /*
            Создание и открытие окна
         */
        CropDialog.prototype.openDialog = function(options) {
            var $template = $('<div/>').addClass('preload').appendTo('body');
            this.$dialog = $template.dialog(options.dialog_opts);
        };


        /*
            Закрытие окна
         */
        CropDialog.prototype.closeDialog = function() {
            if (this.$dialog && this.$dialog.length) {
                this.$dialog.dialog('close');
            }
        };


        /*
            Событие открытия окна
         */
        CropDialog.prototype.onDialogOpen = function($button, options) {
            var that = this;

            // начальные занчения отношения размеров
            this.preview_relation_x = 1;
            this.preview_relation_y = 1;

            setTimeout(function() {
                $.loadImageDeferred(options.image).always(function() {
                    that.$dialog.removeClass('preload');
                }).done(function(img) {
                    // картинка загружена
                    var $image = $('<img>').attr({
                        src: img.src
                    }).css({
                        // maxWidth: that.opts.dialog_image_max_size[0],
                        // maxHeight: that.opts.dialog_image_max_size[1]
                    });

                    that.$dialog.prepend($image);

                    // отношение реальных размеров картинки к
                    // картинке в окне
                    that.preview_relation_x = $image.prop('naturalWidth') / $image.width();
                    that.preview_relation_y = $image.prop('naturalHeight') / $image.height();

                    // Инициализация jCrop
                    $image.Jcrop({
                        keySupport: false,
                        bgOpacity: 0.3,
                        boxWidth: that.opts.dialog_image_max_size[0],
                        boxHeight: that.opts.dialog_image_max_size[1],
                        boundary: 0
                    }, function() {
                        that.jcrop_api = this;

                        // Ограничения размеров
                        if (options.min_size) {
                            var minSize = [
                                Math.ceil(options.min_size[0] / that.preview_relation_x),
                                Math.ceil(options.min_size[1] / that.preview_relation_y)
                            ];
                            that.jcrop_api.setOptions({minSize: minSize});
                            that.jcrop_api.setSelect([0,0].concat(minSize));
                        }
                        if (options.max_size) {
                            var maxSize = [
                                Math.floor(options.max_size[0] / that.preview_relation_x),
                                Math.floor(options.max_size[1] / that.preview_relation_y)
                            ];
                            that.jcrop_api.setOptions({maxSize: maxSize})
                        }

                        // Аспекты
                        if (options.aspects) {
                            that.jcrop_api.setOptions({aspectRatio: options.aspects[0]});
                        }

                        // Положение кропа
                        if (options.cropcoords) {
                            var preview_crop_x = options.cropcoords[0] / that.preview_relation_x;
                            var preview_crop_y = options.cropcoords[1] / that.preview_relation_y;
                            var preview_crop_w = options.cropcoords[2] / that.preview_relation_x;
                            var preview_crop_h = options.cropcoords[3] / that.preview_relation_y;

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

                    img = null;
                }).fail(function() {
                    that.closeDialog();
                });
            }, 100);
        };


        /*
            Событие закрытия окна
         */
        CropDialog.prototype.onDialogClose = function($button, options) {
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
            Отмена обрезки
         */
        CropDialog.prototype.cancelCrop = function($button, options) {
            this.opts.onCancel.call(this, $button);
            this.closeDialog();
        };


        /*
            Применение обрезки
         */
        CropDialog.prototype.applyCrop = function($button, options) {
            var coords = this.jcrop_api.tellSelect();

            // рассчет области обрезки с учетом уменьшения картинки в окне
            var real_coords = [
                Math.round(this.preview_relation_x * coords.x),
                Math.round(this.preview_relation_y * coords.y),
                Math.round(this.preview_relation_x * coords.w),
                Math.round(this.preview_relation_y * coords.h)
            ];

            this.opts.onCrop.call(this, $button, real_coords);
            this.closeDialog();
        };

        return CropDialog;
    })();


    $.fn.cropdialog = function(event, selector, options) {
        var settings = $.extend(true, {}, options, {
            eventType: event,
            buttonSelector: selector
        });

        return this.each(function() {
            CropDialog.create(this, settings);
        });
    };

})(jQuery);
