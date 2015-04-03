(function($) {

    var InitPluploader = function(editor) {
        // Вычисляем размеры превьюх в соответсвии с пропорциями результата
        var aspect = editor.config.PAGEPHOTOS_PHOTO_SIZE[1] / editor.config.PAGEPHOTOS_PHOTO_SIZE[0],
            thumb_width = 120,
            thumb_height = Math.round(thumb_width * aspect);

        $("#ckupload").plupload({
            runtimes : 'html5,flash,silverlight,html4',
            url : editor.config.PAGEPHOTOS_UPLOAD_URL,
            max_file_size : editor.config.PAGEPHOTOS_MAX_FILE_SIZE,
            chunk_size: '256kb',
            file_data_name: 'image',
            headers: {
                'X-CSRFToken': $.cookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            filters : [
               {title : "Image files", extensions : "jpg,jpeg,gif,png,bmp,tif,tiff"}
            ],
            unique_names : true,
            prevent_duplicates: true,
            sortable: true,
            dragdrop: true,
            autostart: true,
            thumb_width: thumb_width,
            thumb_height: thumb_height,
            views: {
               list: false,
               thumbs: true,
               default: 'thumbs'
            },
            flash_swf_url : editor.config.MOXIE_SWF,
            silverlight_xap_url : editor.config.MOXIE_XAP,

            start: function() {
                var ckDialog = CKEDITOR.dialog.getCurrent();
                ckDialog._.buttons['ok'].disable()
            },

            complete: function() {
                var ckDialog = CKEDITOR.dialog.getCurrent();
                ckDialog._.buttons['ok'].enable()
            },

            uploaded: function(event, object) {
                var response = JSON.parse(object.data.response);
                object.file.result_tag = response.tag;

                // Записываем id сохраненных картинок в форму
                var text_field = $('#id_' + response.field);
                if (text_field.length) {
                    var pagephotos = text_field.siblings('input[name="' + response.field + '-page-photos"]');
                    if (!pagephotos.length) {
                        pagephotos = $('<input type="hidden" name="' + response.field + '-page-photos">');
                        text_field.before(pagephotos);
                    }

                    // Формируем список id загруженных картинок
                    var value = pagephotos.val() || '';
                    if (value) {
                        value += ',' + response.id
                    } else {
                        value = response.id
                    }

                    pagephotos.val(value);
                }
            }, 
            error: function(event, object) {
                var err = object.error;
                object.up.removeFile(err.file);
                
                if (err.response) {
                    try {
                        var response = JSON.parse(err.response);
                        alert(response.message);
                        return
                    } catch(e) {}
                };
                
                alert(err.message);
            }
        })
    };

    CKEDITOR.dialog.add("pagephotos", function (editor) {
		return {
            title: gettext('Upload images'),
            minWidth: 680,
            minHeight: 400,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    type: 'html',
                    html: '<div id="ckupload">' + gettext('Uploading...') + '</div>'
                }]
            }],

            onLoad: function() {
                this._.element.$.id = 'ckupload_dialog';

                // CSS приходится грузить JS-ом из-за переопределения стилей
                if (editor.config.PLUPLOADER_CSS) {
                    for (var i=0, l=editor.config.PLUPLOADER_CSS.length; i<l; i++) {
                        CKEDITOR.document.appendStyleSheet(editor.config.PLUPLOADER_CSS[i])
                    }
                }

                // Инициализация загрузчика
                InitPluploader(editor)
            },

            onOk: function() {
                var uploader = $('#ckupload'),
                    images=[],
                    not_loaded = [],
                    file,
                    img,
                    file_index,
                    tag_index;

                // Очистка очереди и получение тегов изображений
                var files = uploader.plupload('getFiles');
                for (file_index=files.length-1; file_index>=0; file_index--) {
                    file = files[file_index];
                    if (file.status == 1) {
                        not_loaded.push(file);
                    } else {
                        if (file.status == 5) {
                            images.push(file.result_tag.trim());
                        }

                        uploader.plupload('removeFile', file)
                    }
                }

                if (not_loaded.length) {
                    var need_load = confirm(gettext('There are not uploaded images.\nUpload them now?'));

                    if (need_load) {
                        uploader.plupload('start');
                        return false
                    }
                }

                if (images.length) {
                    //Вставка картинок
					var container = editor.getSelection().getStartElement();
					if (container.hasClass('page-images')) {
						if (images.length) {
							for (tag_index=images.length-1; tag_index>=0; tag_index--) {
								editor.insertHtml(images[tag_index])
							}
						}
					} else {
						container = editor.document.createElement('p');
						container.addClass('page-images');
						if (images.length) {
							for (tag_index=images.length-1; tag_index>=0; tag_index--) {
								container.appendHtml(images[tag_index])
							}
							editor.insertElement(container)
						}
					}

					// Определение типа галереи
                    if (container.getElementsByTag('img').count() > 1) {
						container
							.removeClass('single-image')
							.addClass('multi-image')
					} else {
						container
							.removeClass('multi-image')
							.addClass('single-image')
					}
                }
            },

            onCancel: function() {
                // Очистка очереди
                var uploader = $('#ckupload');
                var files = uploader.plupload('getFiles');
                for (var file_index=files.length-1; file_index>=0; file_index--) {
                    uploader.plupload('removeFile', files[file_index])
                }
            }
        }
	})

})(jQuery);