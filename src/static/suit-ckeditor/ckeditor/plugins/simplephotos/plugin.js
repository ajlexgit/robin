(function() {

    var InitUploader = function(editor, path) {
        var fake = editor.document.createElement('button');

        var uploader = new plupload.Uploader({
            runtimes : 'html5,flash,silverlight,html4',
            url : editor.config.SIMPLEPHOTOS_UPLOAD_URL,
            browse_button : fake.$,
            drop_element: editor.document.$.documentElement,
            chunk_size: '256kb',
            file_data_name: 'image',
            resize: editor.config.SIMPLEPHOTOS_PHOTO_SIZE,
            headers: {
                'X-CSRFToken': $.cookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            filters : {
                max_file_size : editor.config.SIMPLEPHOTOS_MAX_FILE_SIZE,
                mime_types: [
                    {title : "Image files", extensions : "jpg,jpeg,gif,png,bmp,tif,tiff"}
                ]
            },
            unique_names : true,
            flash_swf_url : editor.config.MOXIE_SWF,
            silverlight_xap_url : editor.config.MOXIE_XAP,
            init: {
                FilesAdded: function(up, files) {
                    plupload.each(files, function(file) {
                        var preloader = editor.document.createElement('img');
                        preloader.addClass('simple-photo');
                        preloader.setAttribute('id', file.id);
                        preloader.setAttribute('src', path + 'preloader.gif');
                        editor.insertElement(preloader);
                    });

                    // Старт загрузки сразу после добавления
                    up.start();
                },

                FileUploaded: function(up, file, data) {
                    // Файл загружен
                    var response = JSON.parse(data.response);
                    var preloader = editor.document.getById(file.id);
                    if (preloader) {
                        preloader.setAttribute('src', response.url);
                    }

                    var text_field = $('#id_' + response.field);
                    if (text_field.length) {
                        var simplephotos = text_field.siblings('input[name="' + response.field + '-simple-photos"]');
                        if (!simplephotos.length) {
                            simplephotos = $('<input type="hidden" name="' + response.field + '-simple-photos">');
                            text_field.before(simplephotos);
                        }

                        // Формируем список id загруженных картинок
                        var value = simplephotos.val() || '';
                        if (value) {
                            value += ',' + response.id
                        } else {
                            value = response.id
                        }

                        simplephotos.val(value);
                    }
                },

                Error: function(up, err) {
                    var preloader = editor.document.getById(err.file.id);
                    if (preloader) {
                        preloader.remove()
                    }

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
        return uploader;
    };

    CKEDITOR.plugins.add("simplephotos", {
        init: function (editor) {
            var c = editor.addCommand("simplephotos", new CKEDITOR.dialogCommand("simplephotos", {
                allowedContent: 'img(!simple-photo)[!src,alt,width,height,title,data-id]'
            }));
            c.modes = {
                wysiwyg: 1,
                source: 0
            };
            c.canUndo = true;

            var path = this.path;
            editor.on('contentDom', function () {
                InitUploader(editor, path);
            });
        }
    })

})();
