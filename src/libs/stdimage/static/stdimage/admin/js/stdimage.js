(function($) {


    var StdImage = Class(null, function(cls, superclass) {
        var MIN_WIDTH_ERROR = gettext('Image should not be less than %(limit)spx in width');
        var MIN_HEIGHT_ERROR = gettext('Image should not be less than %(limit)spx in height');
        var MAX_WIDTH_ERROR = gettext('Image should not be more than %(limit)spx in width');
        var MAX_HEIGHT_ERROR = gettext('Image should not be more than %(limit)spx in height');

        cls.init = function(root) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                console.error('StdImage: root element not found');
                return false;
            }

            // превью
            this.$previews = this.$root.find('.item-preview').first();
            if (!this.$previews.length) {
                console.error('StdImage: previews block not found');
                return false;
            }

            // инпут
            this.$input = this.$root.find('input[type="file"]').first();
            if (!this.$input.length) {
                console.error('StdImage: previews block not found');
                return false;
            }

            // обертка кнопки обрезки
            this.$crop_btn_wrapper = this.$root.find('.crop-btn-wrapper').first();

            // настройки
            this.opts = this.getOpts();

            this.$root.data(cls.dataParamName, this);
        };

        /*
            Получение всех настроек поля
         */
        cls.prototype.getOpts = function() {
            var opts = {};
            var data = this.$root.data();

            // путь к исходнику (для cropdialog)
            opts.source_url = data.source;

            // аспекты кропа (для cropdialog)
            opts.aspects = data.aspects;

            // размер админской превью
            opts.target_size = data.size || '';
            if (!$.isArray(opts.target_size)) {
                opts.target_size = String(opts.target_size).split('x');
            }
            opts.target_size = opts.target_size.map(function(item) {
                return parseInt(item);
            }).filter($.isNumeric).slice(0, 2);

            // можно ли обрезать картинку
            opts.crop = parseInt(data.crop);

            // можно ли растягивать картинку
            opts.stretch = parseInt(data.stretch);

            // максимальная ширина и высота контента картинки (для crop = False).
            // Эти параметры описывают ограничения размеров картинки
            // в случаях, когда в size один из параметров равен 0.
            opts.max_width = parseInt(data.max_width);
            opts.max_height = parseInt(data.max_height);

            // Смещение картинки (отношение разницы размеров по горизонтали и вертикали)
            opts.offset = data.offset || '';
            if (!$.isArray(opts.offset)) {
                opts.offset = String(opts.offset).split('x');
            }
            opts.offset = opts.offset.map(function(item) {
                return parseFloat(item);
            }).filter($.isNumeric).slice(0, 2);

            // Смещение картинки (относительное положение центра накладываемой картинки)
            opts.center = data.center || '';
            if (!$.isArray(opts.center)) {
                opts.center = String(opts.center).split('x');
            }
            opts.center = opts.center.map(function(item) {
                return parseFloat(item);
            }).filter($.isNumeric).slice(0, 2);

            // Цвет фона
            opts.background = data.background || '255,255,255,0';
            if (!$.isArray(opts.background)) {
                opts.background = String(opts.background).split(',');
            }
            opts.background = opts.background.map(function(item) {
                return parseInt(item);
            }).filter($.isNumeric).slice(0, 4);


            // минимальный размер исходника
            opts.min_dimensions = data.min_dimensions || '';
            if (!$.isArray(opts.min_dimensions)) {
                opts.min_dimensions = String(opts.min_dimensions).split('x');
            }
            opts.min_dimensions = opts.min_dimensions.map(function(item) {
                return parseInt(item);
            }).filter($.isNumeric).slice(0, 2);

            // максимальный размер исходника
            opts.max_dimensions = data.max_dimensions || '';
            if (!$.isArray(opts.max_dimensions)) {
                opts.max_dimensions = String(opts.max_dimensions).split('x');
            }
            opts.max_dimensions = opts.max_dimensions.map(function(item) {
                return parseInt(item);
            }).filter($.isNumeric).slice(0, 2);

            return opts;
        };

        /*
            Загрузка файла для создания превью
         */
        cls.prototype.readFile = function(success) {
            var that = this;
            var file = this.$input.prop('files').item(0);

            this.$previews.addClass('preloader').show();

            $.fileReaderDeferred(file).done(function(src) {
                $.loadImageDeferred(src).done(function(img) {
                    that.$crop_btn_wrapper.show();

                    // для cropdialog
                    that.opts.source_url = src;

                    that.showPreview(img);

                    success.call(that, img);

                    that.$previews.removeClass('preloader');
                }).fail(function(reason) {
                    // ошибка разбора изображения
                    that._badfile();
                    that.$previews.hide();
                    if (reason == 'Not image') {
                        alert(gettext('File is not an image'));
                    } else {
                        console.error(reason);
                    }
                });
            }).fail(function(reason) {
                // ошибка загрузки файла
                that._badfile();
                that.$previews.hide();
                if (reason != 'Not a file') {
                    alert(reason);
                }
            });
        };

        /*
            Ошибка загрузки файла для создания превью
         */
        cls.prototype._badfile = function() {
            this.$input.val('');
            this.$previews.removeClass('preloader');

            // для cropdialog
            this.opts.source_url = '';

            this.$crop_btn_wrapper.hide();
        };

        /*
            Показ превью картинки source, обрезанной по области coords
         */
        cls.prototype.showPreview = function(img, coords) {
            var canvas = $.previewCanvas({
                source: img,
                width: this.opts.target_size[0],
                height: this.opts.target_size[1],
                crop: this.opts.crop,
                stretch: this.opts.stretch,
                max_width: this.opts.max_width,
                max_height: this.opts.max_height,
                coords: coords,
                offset: this.opts.offset,
                center: this.opts.center,
                background: this.opts.background
            });
            this.$previews.empty();
            var $image = $('<img/>').attr('src', canvas.toDataURL());
            this.$previews.prepend($image);
        };

        /*
            Валидация размеров картинки
         */
        cls.prototype.validate = function(source) {
            if (this.opts.min_dimensions[0] && (source.width < this.opts.min_dimensions[0])) {
                this.setError(MIN_WIDTH_ERROR, {
                    limit: this.opts.min_dimensions[0]
                });

                this._badfile();
                return
            }

            if (this.opts.min_dimensions[1] && (source.height < this.opts.min_dimensions[1])) {
                this.setError(MIN_HEIGHT_ERROR, {
                    limit: this.opts.min_dimensions[1]
                });
                return
            }

            if (this.opts.max_dimensions[0] && (source.width > this.opts.max_dimensions[0])) {
                this.setError(MAX_WIDTH_ERROR, {
                    limit: this.opts.min_dimensions[0]
                });
                return
            }

            if (this.opts.max_dimensions[1] && (source.height > this.opts.max_dimensions[1])) {
                this.setError(MAX_HEIGHT_ERROR, {
                    limit: this.opts.max_dimensions[1]
                });
                // return
            }
        };

        /*
            Показ ошибки поля
         */
        cls.prototype.setError = function(msg, data) {
            var text = interpolate(msg, data, true);
            this.$previews.addClass('invalid').append(
                $('<span>').addClass('error').text(text)
            )
        };

        /*
            Очистка ошибок поля
         */
        cls.prototype.clearErrors = function() {
            this.$previews.removeClass('invalid');
            this.$previews.find('.error').remove();
        };
    });
    StdImage.dataParamName = 'stdimage';


    /*
        Изменение файла в поле stdimage
     */
    $(document).on('change', '.stdimage', function() {
        var stdimage = $(this).data(StdImage.dataParamName);
        if (!stdimage) {
            console.error('StdImage object not found');
            return false;
        }

        stdimage.clearErrors();

        // сброс обрезки
        stdimage.$crop_btn_wrapper.find('input').val('');

        // загрузка картинки и показ превью
        stdimage.readFile(function(img) {
            // валидация
            this.validate(img);
        });
    });


    $(document).ready(function() {
        $('.stdimage').each(function() {
            var $this = $(this);
            if (!$this.closest('.empty-form').length) {
                StdImage.create($this);
            }
        });

        if (window.Suit) {
            Suit.after_inline.register('stdimage', function(inline_prefix, row) {
                row.find('.stdimage').each(function() {
                    StdImage.create(this);
                });
            });
        }


        // Обрезка картинки
        CropDialog.create(document, {
            eventTypes: 'click.cropdialog',
            buttonSelector: '.stdimage .crop-btn-wrapper button',

            beforeOpen: function($button) {
                this.$field = $button.closest('.stdimage');
                this.stdimage = this.$field.data(StdImage.dataParamName);
                if (!this.stdimage) {
                    console.error('CropDialog: StdImage not found');
                    return false;
                }
            },

            getImage: function() {
                return this.stdimage.opts.source_url;
            },
            getMinSize: function() {
                return this.formatSize(this.stdimage.opts.min_dimensions);
            },
            getMaxSize: function() {
                return this.formatSize(this.stdimage.opts.max_dimensions);
            },
            getAspects: function() {
                return this.formatAspects(this.stdimage.opts.aspects);
            },
            getCropCoords: function() {
                return this.formatCoords(this.stdimage.$crop_btn_wrapper.find('input').val());
            },

            onCrop: function($button, coords) {
                var source_url = this.opts.getImage.call(this, $button);
                if (source_url.substr(0, 4) != 'data') {
                    source_url += '?_=' + Math.random().toString().substr(2);
                }

                // загружаем исходник и обрезаем его по выбранной области
                var that = this;
                this.stdimage.$previews.addClass('preloader');
                $.loadImageDeferred(source_url).done(function(img) {
                    that.stdimage.showPreview(img, coords);
                    that.stdimage.$previews.removeClass('preloader');
                });

                // Записываем координаты в форму
                this.stdimage.$crop_btn_wrapper.find('input').val(coords.join(':'));
            }
        });
    });

})(jQuery);
