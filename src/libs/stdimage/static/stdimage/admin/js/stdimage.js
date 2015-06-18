(function($) {

    var positionImage = function($preview, source, coords) {
        var $image = $preview.find('img');
        var action_id = parseInt($preview.data('action')) || 1;

        // target
        var target_size = $preview.data('size') || '';
        if (!$.isArray(target_size)) {
            target_size = String(target_size).split('x');
        }
        target_size = target_size.map(function(item) {
            return parseInt(item);
        }).filter($.isNumeric).slice(0, 2);

        // position
        var position = $preview.data('position') || '';
        if (!$.isArray(position)) {
            position = String(position).split('x');
        }
        position = position.map(function(item) {
            return parseFloat(item);
        }).filter($.isNumeric).slice(0, 2);

        // background
        var background = $preview.data('background') || '255,255,255,0';
        if (!$.isArray(background)) {
            background = String(background).split(',');
        }
        background = background.map(function (item) {
            return parseInt(item);
        }).filter($.isNumeric).slice(0, 4);

        var canvas;
        if (action_id == 1) {
            // crop
            canvas = $.cropToCanvas({
                source: source,
                width: target_size[0],
                height: target_size[1],
                coords: coords
            });
            $image.attr('src', canvas.toDataURL());
        } else if (action_id == 2) {
            // crop anyway
            canvas = $.cropAnywayToCanvas({
                source: source,
                width: target_size[0],
                height: target_size[1],
                coords: coords
            });
            $image.attr('src', canvas.toDataURL());
        } else if (action_id == 3) {
            // stretch by width
            canvas = $.stretchByWidthToCanvas({
                source: source,
                width: target_size[0],
                height: target_size[1],
                coords: coords
            });
            $image.attr('src', canvas.toDataURL());
        } else if (action_id == 4) {
            // inscribe
            canvas = $.inscribeToCanvas({
                source: source,
                width: target_size[0],
                height: target_size[1],
                coords: coords,
                position: position,
                background: background
            });
            $image.attr('src', canvas.toDataURL());
        } else {
            $.placeImage($preview, $image, coords);
        }
    };

    $(document).on('change', '.stdimage .uploader', function() {
        var $input = $(this),
            $block = $input.closest('.stdimage'),
            $preview = $block.find('.item-preview').addClass('preloader').empty(),
            preview_data = $preview.data(),
            $crop_btn_wrapper = $block.find('.crop-btn-wrapper');

        $.fileReaderDeferred($input.prop('files').item(0)).done(function(src) {
            $.imageDeferred(src).done(function(img) {
                var $image = $('<img/>');
                $crop_btn_wrapper.removeClass('hide').find('button').removeData('crop');
                $preview.empty().removeClass('hide preloader').css({
                    background: 'none'
                }).append($image);

                preview_data.source = src;
                $image.attr('src', preview_data.source);

                positionImage($preview, img);
            }).fail(function(reason) {
                $input.val('');
                $preview.removeClass('preloader').addClass('hide');
                preview_data.source = '';

                if (reason == 'Not image') {
                    alert(gettext('Файл не является изображением'));
                } else {
                    console.error(reason);
                }
            });
        }).fail(function(reason) {
            $input.val('');
            $preview.removeClass('preloader').addClass('hide');
            preview_data.source = '';

            if (reason != 'Not a file') {
                alert(reason);
            }
        });
    });


    $(document).cropdialog('click.cropdialog', '.stdimage .crop-btn-wrapper button', {
        image_url: function($element) {
            var $block = $element.closest('.stdimage'),
                $preview = $block.find('.item-preview');
            return $preview.data('source');
        },
        min_size: function($element) {
            return $element.data('min_dimensions');
        },
        max_size: function($element) {
            return $element.data('max_dimensions');
        },
        aspect: function($element) {
            return $element.data('aspects');
        },
        crop_position: function($element) {
            var crop_position = $element.data('crop');
            if (crop_position) {
                return crop_position;
            }
            // Имя поля, в котором хранится значение кропа
            var crop_field_name = $element.data('crop_field') || '';
            if (crop_field_name) {
                return;
            }

            // Форматируем имя в случае формсетов
            var input = $element.closest('.stdimage').find('input[type="file"]');
            var name = input.attr('name');
            if (name.indexOf('-') >= 0) {
                var formset_prefix = name.split('-').slice(0, -1).join('-');
                crop_field_name = crop_field_name.replace('__prefix__', formset_prefix);
            }
            return $('#id_' + crop_field_name).val();
        },
        onCrop: function($element, coords) {
            var $preview = $element.closest('.stdimage').find('.item-preview');
            var $image = $preview.find('img');

            // Загружаем исходник и позиционируем его
            var source_url = $preview.data('source');
            if (source_url.substr(0, 4) != 'data') {
                source_url += '?_=' + Math.random().toString().substr(2);
            }
            $.imageDeferred(source_url).done(function(img) {
                $image.attr('src', img.src);
                positionImage($preview, img, coords);
            });

            // Записываем координаты в форму
            var coords_text = coords.join(':');
            $element.next('input').val(coords_text);
            $element.data('crop', coords_text);

            // Имя поля, в котором хранится значение кропа
            var crop_field_name = $element.data('crop_field') || '';
            if (crop_field_name) {
                return;
            }

            var input = $element.closest('.stdimage').find('input[type="file"]');
            var name = input.attr('name');
            if (name.indexOf('-') >= 0) {
                var formset_prefix = name.split('-').slice(0, -1).join('-');
                crop_field_name = crop_field_name.replace('__prefix__', formset_prefix);
            }
            $('#id_' + crop_field_name).val(coords_text);
        }
    });

})(jQuery);