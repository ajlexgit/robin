(function($) {

    var InitPluploader = function(editor) {
        $(".ckupload-page-files").plupload({
            runtimes : 'html5,flash,silverlight,html4',
            url : editor.config.PAGEFILES_UPLOAD_URL,
            max_file_size : editor.config.PAGEFILES_MAX_FILE_SIZE,
            chunk_size: '256kb',
            file_data_name: 'file',
            headers: {
                'X-CSRFToken': $.cookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            unique_names : true,
            prevent_duplicates: true,
            sortable: true,
            dragdrop: true,
            autostart: true,
            views: {
               list: true,
               thumbs: false,
               default: 'list'
            },
            flash_swf_url : editor.config.MOXIE_SWF,
            silverlight_xap_url : editor.config.MOXIE_XAP,

            init: {
                BeforeUpload: function() {
                    var ckDialog = CKEDITOR.dialog.getCurrent();
                    ckDialog._.buttons['ok'].disable();
                    ckDialog._.buttons['cancel'].disable();
                },
                FileUploaded: function(up, file, data) {
                    var response = $.parseJSON(data.response);
                    file.result_tag = response.tag;

                    // Записываем id сохраненных файлов в форму
                    var text_field = $('#id_' + response.field);
                    if (text_field.length) {
                        var pagefiles = text_field.siblings('input[name="' + response.field + '-page-files"]');
                        if (!pagefiles.length) {
                            pagefiles = $('<input type="hidden" name="' + response.field + '-page-files">');
                            text_field.before(pagefiles);
                        }

                        // Формируем список id загруженных файлов
                        var value = pagefiles.val() || '';
                        if (value) {
                            value += ',' + response.id
                        } else {
                            value = response.id
                        }

                        pagefiles.val(value);
                    }
                },
                UploadComplete: function(up, files) {
                    var ckDialog = CKEDITOR.dialog.getCurrent();
                    ckDialog._.buttons['ok'].enable();
                    ckDialog._.buttons['cancel'].enable();
                },
                Error: function(up, error) {
                    up.removeFile(error.file);

                    if (error.response) {
                        try {
                            var response = $.parseJSON(error.response);
                            alert(response.message);
                            return
                        } catch (e) {
                        }
                    }
                    alert(error.message);
                }
            }
        })
    };

    CKEDITOR.dialog.add("pagefiles", function (editor) {
        return {
            title: gettext('Upload files'),
            minWidth: 600,
            minHeight: 400,
            contents: [{
                id: 'tab-basic-files',
                label: 'Basic Settings',
                elements: [{
                    type: 'html',
                    html: '<div class="ckupload-files ckupload-page-files">' + gettext('Loading...') + '</div>'
                }]
            }],

            onLoad: function() {
                $(this._.element.$).addClass('ckupload_dialog');

                // CSS приходится грузить JS-ом из-за переопределения стилей
                if (editor.config.PLUPLOADER_CSS) {
                    for (var i=0, l=editor.config.PLUPLOADER_CSS.length; i<l; i++) {
                        CKEDITOR.document.appendStyleSheet(editor.config.PLUPLOADER_CSS[i])
                    }
                }

                // Инициализация загрузчика
                InitPluploader(editor);
            },

            onOk: function() {
                var uploader = $('.ckupload-page-files'),
                    uploaded=[],
                    not_loaded = [],
                    file,
                    file_index,
                    tag_index;

                // Очистка очереди и получение тегов
                var files = uploader.plupload('getFiles');
                for (file_index=files.length-1; file_index>=0; file_index--) {
                    file = files[file_index];
                    if (file.status == 1) {
                        not_loaded.push(file);
                    } else {
                        if (file.status == 5) {
                            uploaded.push(file.result_tag.trim());
                        }

                        uploader.plupload('removeFile', file)
                    }
                }

                if (not_loaded.length) {
                    var need_load = confirm(gettext('There are not uploaded files.\nUpload them now?'));
                    if (need_load) {
                        uploader.plupload('start');
                        return false
                    }
                }

                if (uploaded.length) {
                    // Вставка файла
                    var output;
                    var container = editor.getSelection().getStartElement();
                    if (container.hasClass('page-files')) {
                        // UL
                        for (tag_index = uploaded.length - 1; tag_index >= 0; tag_index--) {
                            output = CKEDITOR.dom.element.createFromHtml(uploaded[tag_index], editor.document);
                            editor.insertElement(element);
                        }
                    } else {
                        var ascendant = container.getAscendant('ul');
                        var inFiles = ascendant && ascendant.hasClass('page-files');
                        if (inFiles) {
                            container = ascendant;
                        } else {
                            container = editor.document.createElement('ul');
                            container.addClass('page-files');
                        }

                        for (tag_index = uploaded.length - 1; tag_index >= 0; tag_index--) {
                            output = CKEDITOR.dom.element.createFromHtml(uploaded[tag_index], editor.document);
                            container.append(output)
                        }

                        if (!inFiles) {
                            editor.insertElement(container);
                        }
                    }
                }
            },

            onCancel: function() {
                // Очистка очереди
                var $uploader = $('.ckupload-page-files');
                var files = $uploader.plupload('getFiles');
                for (var file_index=files.length-1; file_index>=0; file_index--) {
                    $uploader.plupload('removeFile', files[file_index])
                }
            }
        }
    })

})(jQuery);
