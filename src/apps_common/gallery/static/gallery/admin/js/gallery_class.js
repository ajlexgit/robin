(function($) {

    var formatError = function(file, message, html) {
        var nl = html ? '<br>' : '\n';
        return gettext('Error') + ' "' + file.name + '":' + nl + message;
    };

    var default_options = {
        /*
            Селектор кнопки, к которой будет привязан Pluploader
            для закачки картинок.
        */
        upload_button: '.add-gallery-image'
    };

    /*
        Класс галереи, предоставляющий базовые методы работы над картинками
    */
    window.Gallery = function($container, options) {
        var that = this;
        var query;

        if ($container.data(Gallery.dataParam)) {
            return
        }

        options = $.extend(true, {}, default_options, options);
        that.app_label = $container.children('.app_label').val();
        that.model_name = $container.children('.model_name').val();
        that.field_name = $container.children('.gallery_id').attr('name');
        that.gallery_id = undefined;
        that.uploader = undefined;

        // Создание экземпляра галереи
        that.create = function() {
            if (that.gallery_id) {
                console.info(gettext('Gallery already exists for this entry'));
                return
            }

            if (query) query.abort();
            return query = $.ajax({
                url: window.admin_gallery_create,
                type: 'POST',
                data: {
                    app_label: that.app_label,
                    model_name: that.model_name,
                    field_name: that.field_name
                },
                dataType: 'json',
                success: function(resp) {
                    if (resp) {
                        $container.find('.gallery-wrapper').html(resp.html);
                        that.init(resp.gallery_id);
                    } else {
                        alert(gettext('Failed creation gallery'));
                    }
                },
                error: function() {
                    alert(gettext('Failed creation gallery'));
                }
            });
        };

        that._init_uploader = function() {
            // Клиентский ресайз
            var resize = $container.data('max_source') || '';
            if (resize) {
                resize = String(resize).split('x').map(function(e) {
                    return parseInt(e)
                });
                resize = canvasSize(Math.max(resize[0], 100), Math.max(resize[1], 100));
            } else {
                resize = {};
            }
            // Максимальный вес
            var max_size = $container.data('max_size') || '';
            max_size = Number(max_size) || 0;

            that.uploader = new plupload.Uploader({
                url : window.admin_gallery_upload,
                browse_button : $container.find(options.upload_button).get(0),
                chunk_size: '256kb',
                file_data_name: 'image',
                runtimes : 'html5,flash,silverlight,html4',
                flash_swf_url : '/static/js/plupload/Moxie.swf',
                silverlight_xap_url : '/static/js/plupload/Moxie.xap',
                prevent_duplicates: true,
                resize: resize,
                drop_element : $container.get(0),
                filters : {
                    max_file_size : max_size,
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
                    FilesAdded: function(up, files) {
                        plupload.each(files, function(file) {
                            // Формирование шаблона
                            var $template = $($('#' + that.field_name + '_image_template').html());

                            // Установка ID для дальнейшего обращения
                            $template.attr('id', file.id);

                            $container.find('.gallery-items').append($template);
                        });

                        // Старт загрузки сразу после добавления
                        up.start();
                    },

                    // Начало загрузки файла
                    BeforeUpload: function(up, file) {
                        // Дополнительные параметры
                        up.setOption('multipart_params', {
                            app_label: that.app_label,
                            model_name: that.model_name,
                            field_name: that.field_name,
                            gallery_id: that.gallery_id
                        });

                        var $gallery_item = $('#' + file.id);
                        $gallery_item.addClass('gallery-item-loading');
                    },

                    // Прогресс загрузки файла
                    UploadProgress: function(up, file) {
                        var $gallery_item = $('#' + file.id);
                        $gallery_item.find('.progress-bar').css({
                            width: file.percent + '%'
                        });
                    },

                    // Файл загружен
                    FileUploaded: function(up, file, data) {
                        var $gallery_item = $('#' + file.id),
                            response = JSON.parse(data.response);

                        $gallery_item
                            .removeClass('gallery-item-loading')
                            .data({
                                'source_url': response.source_url,
                                'source_size': response.source_size
                            })
                            .find('.item-id').val(response.id);

                        // Загрузка реального превью
                        $.imageDeferred(
                            response.preview_url
                        ).done(function(img) {
                            $gallery_item.find('.item-show').show();
                            $gallery_item.find('img').attr('src', img.src);
                            $gallery_item.find('.item-preloader').remove();
                            $gallery_item.find('.progress').fadeOut(300);
                        }).fail(function(reason) {
                            console.error(reason);
                        });

                        // callback
                        $container.trigger('item-add.gallery', [$gallery_item, response]);
                    },

                    // Все файлы загружены
                    UploadComplete: function() {
                        that.updateCounter();
                    },

                    // Ошибка загрузки
                    Error: function(up, err) {
                        var $gallery_item = $('#' + err.file.id);
                        var $preview = $gallery_item.find('.item-preloader');
                        var $controls = $gallery_item.find('.item-controls');

                        if ((err.code == plupload.FILE_DUPLICATE_ERROR) || !$gallery_item.length) {
                            alert(formatError(err.file, err.message));
                            return;
                        }

                        $controls.hide();
                        $gallery_item
                            .removeClass('gallery-item-loading')
                            .addClass('gallery-item-error')
                            .find('.progress').fadeOut(500);

                        // Ошибка показывается на фоне превью
                        $.fileReaderDeferred(err.file.getNative()).done(function(src) {
                            $.imageDeferred(src).done(function(img) {
                                src = null;
                                $.imageToCanvasDeferred(img, 600, 600).done(function(canvas) {
                                    img = null;

                                    var $image = $('<img/>').attr('src', canvas.toDataURL());
                                    $preview.find('img').remove();
                                    $preview.prepend($image);
                                    $.placeImage($preview, $image);
                                });
                            }).always(function() {
                                $controls.show();
                            });
                        }).fail(function() {
                            $controls.show();
                        });

                        if (err.response) {
                            try {
                                var response = JSON.parse(err.response);

                                $preview.append(
                                    $('<span>').html(formatError(err.file, response.message, true))
                                );

                                // callback
                                $container.trigger('item-error.gallery', [$gallery_item, response]);
                                return
                            } catch(e) {}
                        }
                        $preview.append(
                            $('<span>').html(formatError(err.file, err.message, true))
                        );

                        // callback
                        $container.trigger('item-error.gallery', [$gallery_item, err]);
                    }
                }
            });

            // Настройки Drag & Drop
            that.uploader.bind('Init', function() {
                if (!that.uploader.features.dragdrop) {
                    return
                }

                var drag_counter = 0;
                $container.on('dragenter.gallery.drag', function() {
                    drag_counter++;
                    if (drag_counter == 1) {
                        $container.addClass('dragover');
                    }
                }).on('dragleave.gallery.drag', function() {
                    drag_counter--;
                    if (drag_counter === 0) {
                        $container.removeClass('dragover');
                    }
                }).on('drop.gallery.drag', function() {
                    drag_counter = 0;
                    setTimeout(function() {
                        $container.removeClass('dragover');
                    }, 0);
                });
            });

            that.uploader.init();
        };

        // Инициализация загрузчика
        that.init = function(gallery_id) {
            if (that.gallery_id) {
                console.info(gettext('Gallery already exists for this entry'));
                return
            }

            that.gallery_id = gallery_id;
            $container.children('.gallery_id').val(that.gallery_id);
            that.updateCounter();

            if (options.upload_button) {
                that._init_uploader();
            }

            // callback
            $container.trigger('init.gallery');
        };

        // Удаление галереи
        that.delete = function() {
            if (!that.gallery_id) {
                console.info(gettext('Gallery does not exist'));
                return
            }

            if (query) query.abort();
            return query = $.ajax({
                url: window.admin_gallery_delete,
                type: 'POST',
                data: {
                    app_label: that.app_label,
                    model_name: that.model_name,
                    gallery_id: that.gallery_id
                },
                success: function(resp) {
                    if (resp) {
                        that.destroy();
                        $container.find('.gallery-wrapper').html(resp);
                    } else {
                        alert(gettext('Failed deletion gallery'));
                    }
                },
                error: function() {
                    alert(gettext('Failed deletion gallery'));
                }
            })
        };

        // Освобождение ресурсов галереи
        that.destroy = function() {
            if (!that.gallery_id) {
                console.info(gettext('Gallery does not exist'));
                return
            }

            that.gallery_id = "";
            $container.children('.gallery_id').val("");
            that.updateCounter();

            if (that.uploader) {
                that.uploader.destroy();
                $container.off('.gallery.drag');
            }

            // callback
            $container.trigger('destroy.gallery');
        };

        // Добавление видео
        that.addVideo = function(link) {
            // Формирование шаблона
            var $gallery_item = $($('#' + that.field_name + '_video_link_template').html()),
                tpl_img = $gallery_item.find('img');

            $gallery_item.find('.item-show').css({
                width: parseInt(tpl_img.attr('width')),
                height: parseInt(tpl_img.attr('height'))
            });
            $container.find('.gallery-items').append($gallery_item);

            $gallery_item.addClass('gallery-item-loading');
            return $.ajax({
                url: window.admin_gallery_upload_video,
                type: 'POST',
                data: {
                    app_label: that.app_label,
                    model_name: that.model_name,
                    gallery_id: that.gallery_id,
                    link: link
                },
                dataType: 'json',
                success: function(response) {
                    $gallery_item.removeClass('gallery-item-loading');
                    $gallery_item.find('.item-id').val(response.id);
                    $gallery_item.find('.item-show').show();
                    $gallery_item.find('img').attr('src', response.preview_url);

                    that.updateCounter();

                    // callback
                    $container.trigger('item-add.gallery', [$gallery_item, response]);
                },
                error: function(data) {
                    var response = data.status == 400 ? JSON.parse(data.responseText) : {};
                    $gallery_item.removeClass('gallery-item-loading');
                    $gallery_item.addClass('gallery-item-error');

                    if (response.message) {
                        alert(response.message);
                    }

                    setTimeout(function() {
                        that.deleteItem($gallery_item);
                    }, 500);

                    // callback
                    $container.trigger('item-error.gallery', [$gallery_item, response]);
                }
            })
        };

        // Удаление элемента галереи
        that.deleteItem = function($item) {
            // Удаление элемента галереи из очереди загрузок
            if (that.uploader) {
                var file = that.uploader.getFile($item.attr('id'));
                if (file) {
                    that.uploader.removeFile(file);
                }
            }

            if ($item.hasClass('gallery-item-error') || $item.hasClass('gallery-item-loading')) {
                // Удаление блока из DOM
                var df = $.Deferred();
                $item.animate({
                    height: 0,
                    width: 0
                }, {
                    duration: 100,
                    complete: function() {
                        $item.remove();

                        // callback
                        df.resolve();
                        $container.trigger('item-delete.gallery', $item);
                    }
                });
                return df.promise();
            } else {
                return $.ajax({
                    url: window.admin_gallery_delete_item,
                    type: 'POST',
                    data: {
                        app_label: that.app_label,
                        model_name: that.model_name,
                        gallery_id: that.gallery_id,
                        item_id: parseInt($item.find('.item-id').val()) || 0
                    },
                    beforeSend: function() {
                        $item.addClass('gallery-item-locked');
                    },
                    success: function() {
                        // Удаление блока из DOM
                        $item.animate({
                            height: 0,
                            width: 0
                        }, {
                            duration: 100,
                            complete: function() {
                                $item.remove();
                                that.updateCounter();

                                // callback
                                $container.trigger('item-delete.gallery', $item);
                            }
                        })
                    },
                    error: function() {
                        $item.removeClass('gallery-item-locked');
                        alert(gettext('Failed deletion item'));
                    }
                })
            }
        };

        // Поворот картинки
        that.rotateItem = function($item, direction) {
            direction = direction || 'left';

            if (query) query.abort();
            return query = $.ajax({
                url: window.admin_gallery_rotate_item + '?direction=' + direction,
                type: 'POST',
                data: {
                    app_label: that.app_label,
                    model_name: that.model_name,
                    gallery_id: that.gallery_id,
                    item_id: parseInt($item.find('.item-id').val()) || 0
                },
                beforeSend: function() {
                    $item.addClass('gallery-item-locked');
                },
                success: function(resp) {
                    $item.find('img').attr({
                        'src': resp.preview_url
                    });
                },
                error: function() {
                    alert(gettext('Failed rotation image'));
                },
                complete: function() {
                    $item.removeClass('gallery-item-locked');
                }
            });
        };

        // Обрезка картинки. Параметр coords - 4 числа, разделенные двоеточием
        that.cropItem = function($item, coords, extra) {
            var data = $.extend({}, extra, {
                app_label: that.app_label,
                model_name: that.model_name,
                gallery_id: that.gallery_id,
                item_id: parseInt($item.find('.item-id').val()) || 0,
                coords: coords
            });

            if (query) query.abort();
            return query = $.ajax({
                url: window.admin_gallery_crop_item,
                type: 'POST',
                data: data,
                beforeSend: function() {
                    $item.addClass('gallery-item-locked');
                },
                success: function(resp) {
                    $item.find('img').attr({
                        'src': resp.preview_url
                    });
                },
                error: function() {
                    alert(gettext('Failed crop image'));
                },
                complete: function() {
                    $item.removeClass('gallery-item-locked');
                }
            });
        };

        // Обновление значения счетчиков картинок
        that.updateCounter = function() {
            var counters = $('.gallery-' + that.field_name + '-counter-image');
            if (counters.length) {
                var items = $container.find('.gallery-item-image:not(.gallery-item-error):not(.gallery-item-loading)');
                counters.text(items.length);
            }

            counters = $('.gallery-' + that.field_name + '-counter-video-link');
            if (counters.length) {
                items = $container.find('.gallery-item-video-link:not(.gallery-item-error):not(.gallery-item-loading)');
                counters.text(items.length);
            }
        };

        $container.data(Gallery.dataParam, that);

        // callback
        $container.trigger('create.gallery');

        // Если галерея существует - инициализируем её
        var gallery_id = $container.children('.gallery_id').val();
        if (gallery_id) {
            that.init(gallery_id);
        }
    };

    window.Gallery.dataParam = 'object';

})(jQuery);