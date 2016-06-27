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
                    var $tag = $(response.tag).addClass('simple-photo');

                    var $doc = $(editor.editable().$);
                    $doc.find('#' + file.id).replaceWith($tag);

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
        lang: 'en,ru',
        init: function(editor) {
            var lang = editor.lang.simplephotos;

            // ======================================
            //      DIALOGS
            // ======================================

            CKEDITOR.dialog.add("simplephotos_image_description", this.path + "dialogs/image_description.js");


            // ======================================
            //      COMMANDS
            // ======================================

            // UPLOAD
            editor.addCommand("simplephotos", new CKEDITOR.dialogCommand("simplephotos", {
                modes: {
                    wysiwyg: 1,
                    source: 0
                },
                canUndo: true
            }));

            // IMAGE DESCRIPTION
            editor.addCommand("simplephotos_image_description", new CKEDITOR.dialogCommand("simplephotos_image_description"));


            // ======================================
            //      CONTEXT MENU
            // ======================================

            // Добавление пунктов в контекстное меню
            editor.addMenuGroup('images');
            editor.addMenuItems({
                _simple_image_description : {
                    label : lang.contextMenuImageDescr,
                    icon: this.path + 'descr.png',
                    command : 'simplephotos_image_description',
                    group : 'images'
                }
            });
            editor.contextMenu.addListener(function(element) {
                if (element && element.is('img') && element.hasClass('simple-photo')) {
                    return {
                        _simple_image_description : CKEDITOR.TRISTATE_OFF
                    }
                }
                return null
            });

            var path = this.path;
            editor.on('contentDom', function() {
                InitUploader(editor, path);
            });
        }
    })

})();
