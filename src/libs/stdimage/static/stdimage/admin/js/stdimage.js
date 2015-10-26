(function($) {

    var positionImage = function($field, $image, source, coords) {
        // target
        var target_size = $field.data('size') || '';
        if (!$.isArray(target_size)) {
            target_size = String(target_size).split('x');
        }
        target_size = target_size.map(function(item) {
            return parseInt(item);
        }).filter($.isNumeric).slice(0, 2);

        // offset
        var offset = $field.data('offset') || '';
        if (!$.isArray(offset)) {
            offset = String(offset).split('x');
        }
        offset = offset.map(function(item) {
            return parseFloat(item);
        }).filter($.isNumeric).slice(0, 2);

        // center
        var center = $field.data('center') || '';
        if (!$.isArray(center)) {
            center = String(center).split('x');
        }
        center = center.map(function(item) {
            return parseFloat(item);
        }).filter($.isNumeric).slice(0, 2);

        // background
        var background = $field.data('background') || '255,255,255,0';
        if (!$.isArray(background)) {
            background = String(background).split(',');
        }
        background = background.map(function(item) {
            return parseInt(item);
        }).filter($.isNumeric).slice(0, 4);

        var crop = parseInt($field.data('crop'));
        var stretch = parseInt($field.data('stretch'));
        var max_width = parseInt($field.data('max_width'));
        var max_height = parseInt($field.data('max_height'));

        var canvas = $.previewCanvas({
            source: source,
            width: target_size[0],
            height: target_size[1],
            crop: crop,
            stretch: stretch,
            max_width: max_width,
            max_height: max_height,
            coords: coords,
            offset: offset,
            center: center,
            background: background
        });
        $image.attr('src', canvas.toDataURL());
    };


    $(document).on('change', '.stdimage .uploader', function() {
        var $input = $(this),
            $field = $input.closest('.stdimage'),
            field_data = $field.data(),
            $preview = $field.find('.item-preview').addClass('preloader').empty(),
            $crop_btn_wrapper = $field.find('.crop-btn-wrapper');

        // сброс обрезки
        $crop_btn_wrapper.find('input').val('');

        $.fileReaderDeferred($input.prop('files').item(0)).done(function(src) {
            $.loadImageDeferred(src).done(function(img) {
                var $image = $('<img/>');
                $crop_btn_wrapper.show();

                $preview
                    .show()
                    .empty()
                    .removeClass('preloader')
                    .css({
                        background: 'none'
                    })
                    .append($image);

                field_data.source = src;
                $image.attr('src', field_data.source);

                positionImage($field, $image, img);
            }).fail(function(reason) {
                $input.val('');
                $preview.removeClass('preloader').hide();
                field_data.source = '';

                if (reason == 'Not image') {
                    alert(gettext('Файл не является изображением'));
                } else {
                    console.error(reason);
                }
            });
        }).fail(function(reason) {
            $input.val('');
            $preview.removeClass('preloader').hide();
            field_data.source = '';

            if (reason != 'Not a file') {
                alert(reason);
            }
        });
    });


    $(document).cropdialog('click.cropdialog', '.stdimage .crop-btn-wrapper button', {
        image_url: function($element) {
            var $field = $element.closest('.stdimage');
            return $field.data('source');
        },
        min_size: function($element) {
            var $field = $element.closest('.stdimage');
            return $field.data('min_dimensions');
        },
        max_size: function($element) {
            var $field = $element.closest('.stdimage');
            return $field.data('max_dimensions');
        },
        aspect: function($element) {
            var $field = $element.closest('.stdimage');
            return $field.data('aspects');
        },
        crop_position: function($element) {
            var $wrapper = $element.closest('.crop-btn-wrapper');
            return $wrapper.find('input').val();
        },
        onCrop: function($element, coords) {
            var $field = $element.closest('.stdimage');
            var $wrapper = $element.closest('.crop-btn-wrapper');
            var $image = $field.find('.item-preview').find('img');

            // Загружаем исходник и позиционируем его
            var source_url = $field.data('source');
            if (source_url.substr(0, 4) != 'data') {
                source_url += '?_=' + Math.random().toString().substr(2);
            }
            $.loadImageDeferred(source_url).done(function(img) {
                $image.attr('src', img.src);
                positionImage($field, $image, img, coords);
            });

            // Записываем координаты в форму
            var coords_text = coords.join(':');
            $wrapper.find('input').val(coords_text);
        }
    });

})(jQuery);
