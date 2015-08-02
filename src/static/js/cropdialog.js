(function($) {

    /*
        Открытие диалогового окна с картинкой для кропа

        Требует:
            jquery.canvas_utils.js, jquery.popups.js

        Настройки:
            // Функция или значение пути к картинке. Если вернет false - диалог не откроется.
            image_url: $.noop,

            // Максимальный размер картинки в окне
            image_box_size: [600, 500],

            // Функция или значение минимального размера обрезки.
            // Формат: "100x100" или [100, 100]
            min_size: $.noop,

            // Функция или значение максимального размера обрезки
            // Формат: "100x100" или [100, 100]
            max_size: $.noop,

            // Функция или значение фиксированных аспектов обрезки
            // Формат: "1.34|1.56" или 1.45 или [1.34, 1.56]
            aspect: $.noop,

            // Начальная позиция окна обрезки
            // Формат: "0:0:100:100" или [0, 0, 100, 100]
            crop_position: $.noop,

            // Опции диалога
            dialog_opts: {},

            // Callback применения обрезки. Если вернет false - диалог не закроется
            onCrop: $.noop,

            // Callback отмены обрезки. Если вернет false - диалог не закроется
            onCancel: $.noop,

            // Callback закрытия окна. Если вернет false - диалог не закроется
            onClose: $.noop
    */

    // Класс диалогового окна кропа
    var CropDialog = function(options) {
        var that = this;
        var dialog, jcrop_api,
            storage = {},
            jcrop_relation_x = 1,
            jcrop_relation_y = 1;

        // Получение значения настройки
        var get_value = function(parameter) {
            var option = options[parameter];
            if ($.isFunction(option)) {
                return option.apply(storage, Array.prototype.slice.call(arguments, 1));
            } else {
                return option
            }
        };

        // Опции окна
        this.dialogOptions = function() {
            var dialog_options = get_value('dialog_opts') || {};
            return $.extend({}, dialog_options, {
                classes: dialog_options.classes + ' preloader',
                content: '<div></div>'
            });
        };

        // Создание окна
        this.create = function($element, image_url) {
            var settings = this.dialogOptions($element, image_url);
            return $.popup(settings).on('before_show', function() {
                that.init($element, image_url);
            }).on('hide', function() {
                that.destroy($element);
            }).show();
        };

        // Инициализация окна
        this.init = function($element, image_url) {
            $.imageDeferred(
                image_url
            ).always(function() {
                dialog.$container.removeClass('preloader');
            }).done(function(img) {
                that.load($element, img);
                img = null;
            }).fail(function() {
                that.close();
            });
        };

        // Картинка загружена
        this.load = function($element, img) {
            var $image = $('<img>').attr({
                src: img.src
            });

            $.popup().update({
                content: [
                    $image,
                    $('<div>').addClass('buttons').append(
                        $('<button/>').addClass('btn btn-ok').on('click', function() {
                            that.crop($element);
                        }).text('OK'),
                        $('<button/>').addClass('btn btn-cancel').on('click', function() {
                            that.cancel($element);
                        }).text('Отмена')
                    )
                ]
            });

            // jCrop
            this.jcrop($element, $image);
        };

        // Инициализация jCrop
        this.jcrop = function($element, $image) {
            var image_box = get_value('image_box_size', $element);

            // min_size
            var min_size = get_value('min_size', $element) || '';
            if (!$.isArray(min_size)) {
                min_size = String(min_size).split('x');
            }
            min_size = min_size.map(function(item) {
                return parseInt(item);
            }).filter($.isNumeric).slice(0, 2);

            // max_size
            var max_size = get_value('max_size', $element) || '';
            if (!$.isArray(max_size)) {
                max_size = String(max_size).split('x');
            }
            max_size = max_size.map(function(item) {
                return parseInt(item);
            }).filter($.isNumeric).slice(0, 2);

            // aspects
            var aspects = get_value('aspect', $element) || '';
            if (!$.isArray(aspects)) {
                aspects = String(aspects).split('|');
            }
            aspects = aspects.map(function(item) {
                return parseFloat(item);
            }).filter($.isNumeric);

            // crop_postition
            var crop_position = get_value('crop_position', $element) || '';
            if (!$.isArray(crop_position)) {
                crop_position = String(crop_position).split(':');
            }
            crop_position = crop_position.map(function(item) {
                return parseInt(item);
            }).filter($.isNumeric).slice(0, 4);

            $image.Jcrop({
                keySupport: false,
                bgOpacity: 0.3,
                boxWidth: image_box[0],
                boxHeight: image_box[1],
                boundary: 0
            }, function() {
                jcrop_api = this;
                jcrop_relation_x = $image.prop('naturalWidth') / $image.width();
                jcrop_relation_y = $image.prop('naturalHeight') / $image.height();

                // Ограничения размеров
                if (min_size.length == 2) {
                    var minSize = [
                        Math.ceil(min_size[0] / jcrop_relation_x),
                        Math.ceil(min_size[1] / jcrop_relation_y)
                    ];
                    this.setOptions({minSize: minSize});
                    this.setSelect([0,0].concat(minSize));
                }
                if (max_size.length == 2) {
                    var maxSize = [
                        Math.floor(max_size[0] / jcrop_relation_x),
                        Math.floor(max_size[1] / jcrop_relation_y)
                    ];
                    this.setOptions({maxSize: maxSize})
                }

                // Аспекты
                if (aspects.length) {
                    this.setOptions({aspectRatio: aspects[0]});
                }

                // Положение кропа
                if (crop_position.length == 4) {
                    crop_position[0] /= jcrop_relation_x;
                    crop_position[1] /= jcrop_relation_y;
                    crop_position[2] /= jcrop_relation_x;
                    crop_position[3] /= jcrop_relation_y;
                    this.setOptions({
                        setSelect: [
                            crop_position[0],
                            crop_position[1],
                            crop_position[0] + crop_position[2],
                            crop_position[1] + crop_position[3]
                        ]
                    });
                }
            });
        };

        // Обрезка
        this.crop = function($element) {
            var coords = jcrop_api.tellSelect();
            var real_coords = [
                Math.round(jcrop_relation_x * coords.x),
                Math.round(jcrop_relation_y * coords.y),
                Math.round(jcrop_relation_x * coords.w),
                Math.round(jcrop_relation_y * coords.h)
            ];

            if (get_value('onCrop', $element, real_coords) === false) {
                return
            }
            this.close();
        };

        // Закрыть окно
        this.close = function() {
            dialog.hide();
        };

        // Деинициализация окна
        this.destroy = function($element) {
            if (get_value('onClose', $element) === false) {
                return false
            }

            if (jcrop_api) {
                jcrop_api.destroy();
                jcrop_api = null;
            }
            dialog = null;
        };

        // Отмена обрезки
        this.cancel = function($element) {
            if (get_value('onCancel', $element) === false) {
                return
            }
            this.close();
        };

        // Наступление целевого события
        this.trigger = function($element) {
            var image_url = get_value('image_url', $element);
            if (!image_url) {
                console.error('cropdialog: ' + gettext('empty image url'));
                return false;
            }

            dialog = this.create($element, image_url);

            return false;
        };
    };

    $.fn.cropdialog = function(event, selector, options) {
        if (typeof selector == 'object') {
            options = selector;
            selector = undefined;
        }

        var settings = $.extend(true, {}, $.fn.cropdialog.defaults, options);
        var crop_object = new CropDialog(settings);
        return this.on(event, selector, function() {
            return crop_object.trigger($(this));
        });
    };

    $.fn.cropdialog.defaults = {
        image_url: $.noop,
        dialog_opts: {},
        image_box_size: [600, 500],
        min_size: $.noop,
        max_size: $.noop,
        aspect: $.noop,
        crop_position: $.noop,
        onCrop: $.noop,
        onCancel: $.noop,
        onClose: $.noop
    };

})(jQuery);
