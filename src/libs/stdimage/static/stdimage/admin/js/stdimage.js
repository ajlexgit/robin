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
        beforeOpen: function($button) {
            this.$field = $button.closest('.stdimage');
        },

        getImage: function($button) {
            return this.$field.data('source');
        },
        getMinSize: function($button) {
            return this.$field.data('min_dimensions');
        },
        getMaxSize: function($button) {
            return this.$field.data('max_dimensions');
        },
        getAspects: function($button) {
            return this.$field.data('aspects');
        },
        getCropCoords: function($button) {
            var $wrapper = $button.closest('.crop-btn-wrapper');
            return $wrapper.find('input').val();
        },
        onCrop: function($button, coords) {
            // Загружаем исходник и позиционируем его
            var source_url = this.opts.getImage.call(this, $button);
            if (source_url.substr(0, 4) != 'data') {
                source_url += '?_=' + Math.random().toString().substr(2);
            }

            var that = this;
            var $image = this.$field.find('.item-preview').find('img');
            $.loadImageDeferred(source_url).done(function(img) {
                $image.attr('src', img.src);
                positionImage(that.$field, $image, img, coords);
            });

            // Записываем координаты в форму
            var $wrapper = $button.closest('.crop-btn-wrapper');
            $wrapper.find('input').val(coords.join(':'));
        }
    });

})(jQuery);
