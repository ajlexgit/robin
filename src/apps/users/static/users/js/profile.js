(function($) {

    // Обновление аватарок на странице
    var change_avatar = function(response) {
        // Обновление кнопок
        $.loadImageDeferred(response.normal_avatar).done(function() {
            $('#profile-avatar').replaceWith(response.profile_avatar_html);
            initUploader();
        });

        $(document).trigger('change_avatar.users', response);
    };

    // Загрузчик аватарки
    var initUploader = function() {
        return Uploader.create('#profile-avatar', {
            url: window.js_storage.avatar_upload,
            buttonSelector: '#upload-avatar',
            multiple: false,
            resize: {
                width: 1024,
                height: 1024
            },
            max_size: '12mb',

            fileUploaded: function(file, json_response) {
                if (json_response) {
                    change_avatar(json_response);
                }
            },
            onError: function(file, error, json_response) {
                if (json_response && json_response.message) {
                    alert(json_response.message)
                }
            }
        });
    };


    // Обрезка аватара
    $(document).cropdialog('click.cropdialog', '#crop-avatar', {
        image_url: function($element) {
            return $element.data('source');
        },
        min_size: function($element) {
            return $element.data('min_dimensions');
        },
        aspect: function($element) {
            return $element.data('aspect');
        },
        crop_position: function($element) {
            return $element.data('crop');
        },
        dialog_opts: {
            classes: 'popup-crop-avatar'
        },
        onCrop: function($element, coords) {
            var coords_str = coords.join(':');
            $.ajax({
                url: window.js_storage.avatar_crop,
                type: 'POST',
                data: {
                    coords: coords_str
                },
                dataType: 'json',
                success: change_avatar
            });
            $element.data('crop', coords_str);
        }
    });


    // Удаление аватара
    $(document).on('click', '.delete-avatar', function() {
        if (!confirm(gettext('Are you sure that you want to delete this avatar?'))) {
            return false;
        }
        $.ajax({
            url: window.js_storage.avatar_delete,
            type: 'POST',
            dataType: 'json',
            success: change_avatar
        });
        return false;
    });


    $(document).ready(function() {
        initUploader();
    });

})(jQuery);
