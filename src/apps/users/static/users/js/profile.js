(function($) {

    var uploader;

    // Обновление аватарок на странице
    var change_avatar = function(response) {
        // Загрузка превью в блоке авторизации
        $.loadImageDeferred(response.small_avatar).done(function(img) {
            $('#auth-block').find('.avatar').attr('src', img.src);
        });

        // Обновление кнопок
        $.loadImageDeferred(response.normal_avatar).done(function() {
            uploader.destroy();
            $('#profile-avatar').replaceWith(response.profile_avatar_html);
            initUploader();
        });
    };

    // Загрузчик аватарки
    var initUploader = function() {
        uploader = new plupload.Uploader({
            url : window.js_storage.avatar_upload,
            browse_button : $('#upload-avatar').get(0),
            chunk_size: '256kb',
            file_data_name: 'image',
            multi_selection: false,
            runtimes : 'html5,flash,silverlight,html4',
            flash_swf_url : window.js_storage.plupload_moxie_swf,
            silverlight_xap_url : window.js_storage.plupload_moxie_xap,
            resize: {
                width: 1024,
                height: 1024
            },
            filters : {
                max_file_size : '12mb',
                mime_types: [
                    {title : "Image files", extensions : "jpg,jpeg,png,bmp,gif"}
                ]
            },
            headers: {
                'X-CSRFToken': $.cookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            init: {
                // Добавление файла в очередь
                FilesAdded: function(up) {
                    // Старт загрузки сразу после добавления
                    up.start();
                },

                // Файл загружен
                FileUploaded: function(up, file, data) {
                    var response = JSON.parse(data.response);
                    change_avatar(response);
                },

                // Ошибка загрузки
                Error: function(up, err) {
                    uploader.removeFile(err.file);
                    if (err.response) {
                        try {
                            var response = JSON.parse(err.response);
                            alert(response.message);
                            return
                        } catch(e) {}
                    }

                    alert(err.message);
                }
            }
        });

        uploader.init();
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
