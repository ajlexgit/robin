(function($) {

    var positionImage = function($preview, source, coords) {
        var $image = $preview.find('img');

        // target
        var target_size = $preview.data('size') || '';
        if (!$.isArray(target_size)) {
            target_size = String(target_size).split('x');
        }
        target_size = target_size.map(function(item) {
            return parseInt(item);
        }).filter($.isNumeric).slice(0, 2);

        // offset
        var offset = $preview.data('offset') || '';
        if (!$.isArray(offset)) {
            offset = String(offset).split('x');
        }
        offset = offset.map(function(item) {
            return parseFloat(item);
        }).filter($.isNumeric).slice(0, 2);

        // center
        var center = $preview.data('center') || '';
        if (!$.isArray(center)) {
            center = String(center).split('x');
        }
        center = center.map(function(item) {
            return parseFloat(item);
        }).filter($.isNumeric).slice(0, 2);

        // background
        var background = $preview.data('background') || '255,255,255,0';
        if (!$.isArray(background)) {
            background = String(background).split(',');
        }
        background = background.map(function(item) {
            return parseInt(item);
        }).filter($.isNumeric).slice(0, 4);

        var crop = parseInt($preview.data('crop'));
        var stretch = parseInt($preview.data('stretch'));
        var max_width = parseInt($preview.data('max_width'));
        var max_height = parseInt($preview.data('max_height'));

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
            $preview = $field.find('.item-preview').addClass('preloader').empty(),
            preview_data = $preview.data(),
            $crop_btn_wrapper = $field.find('.crop-btn-wrapper');

        $.fileReaderDeferred($input.prop('files').item(0)).done(function(src) {
            $.loadImageDeferred(src).done(function(img) {
                var $image = $('<img/>');
                $crop_btn_wrapper.removeClass('hide')
                    .find('button')
                    .removeData('crop')
                    .removeAttr('data-crop');
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
            var $field = $element.closest('.stdimage'),
                $preview = $field.find('.item-preview');
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
            return $element.data('crop') || '';
        },
        onCrop: function($element, coords) {
            var $field = $element.closest('.stdimage');
            var $preview = $field.find('.item-preview');
            var $image = $preview.find('img');

            // Загружаем исходник и позиционируем его
            var source_url = $preview.data('source');
            if (source_url.substr(0, 4) != 'data') {
                source_url += '?_=' + Math.random().toString().substr(2);
            }
            $.loadImageDeferred(source_url).done(function(img) {
                $image.attr('src', img.src);
                positionImage($preview, img, coords);
            });

            // Записываем координаты в форму
            var coords_text = coords.join(':');
            $field.find('input[name$="-croparea"]').val(coords_text);
            $element.data('crop', coords_text);
        }
    });

})(jQuery);
