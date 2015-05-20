(function($) {

    $(document).on('change', '.stdimage .uploader', function() {
        var $input = $(this),
            $block = $input.closest('.stdimage'),
            $preview = $block.find('.item-preview').addClass('preloader'),
            $crop_btn_wrapper = $block.find('.crop-btn-wrapper');

        $.fileReaderDeferred($input.prop('files').item(0)).done(function(src) {
            $.imageDeferred(src).done(function(img) {
                src = null;

                var $image = $('<img/>').attr('src', img.src);
                $crop_btn_wrapper.removeClass('hide').find('button').removeData('crop');
                $preview.find('img').remove();
                $preview.removeClass('hide preloader').css({
                    background: 'none'
                }).prepend($image);
                $.placeImage($preview, $image);
            }).fail(function(reason) {
                $input.val('');
                $preview.removeClass('preloader').addClass('hide');
                if (reason == 'Not image') {
                    alert('Файл не является изображением');
                } else {
                    console.error(reason);
                }
            });
        }).fail(function(reason) {
            $input.val('');
            $preview.removeClass('preloader').addClass('hide');
            if (reason != 'Not a file') {
                alert(reason);
            }
        });
    });


    $(document).cropdialog('click.cropdialog', '.stdimage .crop-btn-wrapper button', {
        image_url: function($element) {
            var $block = $element.closest('.stdimage'),
                new_image = $block.find('.uploader').prop('files').item(0);
            if (new_image) {
                this.new_image = true;
                return $block.find('.item-preview img').prop('src');
            }
            return $element.data('source');
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
            if (this.new_image) {
                $.placeImage($preview, $image, coords);
            } else {
                // Загружаем исходник и позиционируем его
                $.imageDeferred(
                    $element.data('source') + '?_=' + Math.random().toString().substr(2)
                ).done(function(img) {
                    $image.attr('src', img.src);
                    $.placeImage($preview, $image, coords);
                });
            }

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