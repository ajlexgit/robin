(function($) {

    $.fn.gallery = function(options) {
        // actions
        if (typeof options == 'string') {
            switch (options) {
                case 'object':
                    // Получение объекта галереи
                    return this.first().data(Gallery.dataParam);
                case 'destroy':
                    // Уничтожение объекта галереи
                    return this.each(function() {
                        var $container = $(this);
                        var gallery = $container.gallery('object');
                        if (gallery) {
                            gallery.destroy();
                            $container.removeData(Gallery.dataParam)
                        }
                    });
            }
        }

        // Опции галереи
        var settings = $.extend(true, {}, $.fn.gallery.defaults, options);

        // Добавление обработчика по умолчанию, если это разрешено
        var setDefaultEvent = function($elements, event, handler) {
            if (settings.append_existed_events) {
                $elements.on(event, handler);
                return;
            }

            var namespaces = event.split(".");
			var type = namespaces.shift();
			namespaces.sort();
			namespaces = namespaces.join('.');

            $elements.each(function() {
                // Ищем событие с тем же именем
                var events = $._data(this).events[type];
                if (events) {
                    for(var i=0, l=events.length; i<l; i++) {
                        var exist_event = events[i];
                        if ((exist_event.type == type) && (exist_event.namespace == namespaces)) {
                            return true;
                        }
                    }
                }
                $(this).on(event, handler);
            });
        };


        /*
            События по умолчанию
        */

        // Создание объекта Gallery
        setDefaultEvent(this, 'create.gallery', function() {
            var $container = $(this);
            var gallery = $container.gallery('object');

            // Добавляем метод проверки наличия выделенных картинок
            gallery.checkChecked = function() {
                var gallery_items = $container.find('.gallery-items'),
                    checked = gallery_items.find('.gallery-item-checked');
                $container.find('.delete-checked-items').prop('disabled', checked.length == 0);
            };
        });

        // Инициализация диалогового окна обрезки картинок
        setDefaultEvent(this, 'init-cropdialog.gallery', function() {
            var $container = $(this);
            var gallery = $container.gallery('object');

            $container.cropdialog('click.gallery.cropdialog', '.gallery-item .item-crop', {
                image_url: function($element) {
                    return $element.closest('.gallery-item').data('source_url');
                },
                min_size: function() {
                    return $container.find('.min_dimensions').val();
                },
                max_size: function() {
                    return $container.find('.max_dimensions').val();
                },
                aspect: function() {
                    return $container.find('.aspects').val();
                },
                crop_position: function($element) {
                    return $element.data('crop');
                },
                onCrop: function($element, coords) {
                    var coords_str = coords.join(':');
                    gallery.cropItem($element.closest('.gallery-item'), coords_str);
                    $element.data('crop', coords_str);
                }
            });
        });

        // Инициализация объекта Gallery
        setDefaultEvent(this, 'init.gallery', function() {
            var sort_query;
            var $container = $(this);
            var gallery = $container.gallery('object');

            // Диалоговое окно обрезки
            $container.trigger('init-cropdialog.gallery');

            // Сортировка элементов
            $container.find('.gallery-items').sortable({
                containment: "parent",
                helper: 'clone',
                items: '> .gallery-item',
                tolerance: 'pointer',
                distance: 20,
                update: function() {
                    // Сохранение порядка файлов
                    var items = $container.find('.gallery-item'),
                        item_ids = [];

                    items.each(function() {
                        var item_id = parseInt($(this).data('id'));
                        if (item_id) {
                            item_ids.push(item_id)
                        }
                    });

                    if (sort_query) sort_query.abort();
                    sort_query = $.ajax({
                        url: window.admin_gallery_sort,
                        type: 'POST',
                        data: {
                            app_label: gallery.app_label,
                            model_name: gallery.model_name,
                            gallery_id: gallery.gallery_id,
                            item_ids: item_ids.join(',')
                        }
                    })
                }
            }).disableSelection();

            // Выделение картинок и их массовое удаление
            $container.on('change.gallery.checkitem', '.check-box', function() {
                var self = $(this),
                    $item = self.closest('.gallery-item');
                if (self.prop('checked')) {
                    $item.addClass('gallery-item-checked')
                } else {
                    $item.removeClass('gallery-item-checked')
                }
                gallery.checkChecked();
            }).on('click.gallery.checkitem', '.delete-checked-items', function() {
                var gallery_items = $(this).closest('.gallery').find('.gallery-items'),
                    checked = gallery_items.find('.gallery-item-checked');

                var confirm_fmt = ngettext('Are you sure you want to delete checked item?', 'Are you sure you want to delete %s checked items?', checked.length);
                if (!confirm(interpolate(confirm_fmt, [checked.length]))) {
                    return false;
                } else {
                    checked.each(function() {
                        gallery.deleteItem($(this).removeClass('.gallery-item-checked'));
                    });
                    gallery.checkChecked();
                }
                return false;
            });
        });

        // Освобождение ресурсов объекта Gallery
        setDefaultEvent(this, 'destroy.gallery', function() {
            var $container = $(this);

            $container.find('.gallery-items').sortable('destroy');
            $container.off('.gallery.cropdialog');
            $container.off('.gallery.checkitem');
        });

        // Добавлен элемент галереи
        setDefaultEvent(this, 'item-add.gallery', function(event, $item, response) {
            if (response.show_url) {
                $item.find('.item-preview').attr('href', response.show_url);
            }
            $item.find('.check-box').val(response.id);
        });

        // Элемент удалён из галереи
        setDefaultEvent(this, 'item-delete.gallery', function() {
            var $container = $(this);
            var gallery = $container.gallery('object');
            gallery.checkChecked();
        });


        return this.each(function() {
            Gallery.create($(this), settings);
        })
    };


    $.fn.gallery.defaults = {
        /*
            Селектор кнопки, к которой будет привязан Pluploader
            для закачки картинок.
        */
        upload_button: '.add-gallery-image',

        /*
            Если установить false, то обработчики по умолчанию
            не будут добавлены к галерее, если уже существуют
            обработчики с теми же именами.
        */
        append_existed_events: true
    };

})(jQuery);
