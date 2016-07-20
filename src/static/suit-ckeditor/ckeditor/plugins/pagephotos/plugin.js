(function() {

    CKEDITOR.plugins.add("pagephotos", {
        requires: 'dialog',
        icons: 'pagephotos',
        lang: 'en,ru',
        init: function (editor) {
            var lang = editor.lang.pagephotos;

            editor.ui.addButton("PagePhotos", {
                label: lang.buttonTitle,
                command: "pagephotos",
                toolbar: 'insert'
            });

            editor.addContentsCss(this.path + 'styles/editor.css');

            // ======================================
            //      DIALOGS
            // ======================================

            CKEDITOR.dialog.add("pagephotos", this.path + "dialogs/dlg_upload.js");
            CKEDITOR.dialog.add("pagephotos_block_description", this.path + "dialogs/block_description.js");
            CKEDITOR.dialog.add("pagephotos_image_description", this.path + "dialogs/image_description.js");


            // ======================================
            //      COMMANDS
            // ======================================

            // UPLOAD
            editor.addCommand("pagephotos", new CKEDITOR.dialogCommand("pagephotos", {
                allowedContent: 'p(!page-images,single-image,multi-image);',
                modes: {
                    wysiwyg: 1,
                    source: 0
                },
                canUndo: true
            }));

            // BLOCK DESCRIPTION
            editor.addCommand("pagephotos_block_description", new CKEDITOR.dialogCommand("pagephotos_block_description"));

            // IMAGE DESCRIPTION
            editor.addCommand("pagephotos_image_description", new CKEDITOR.dialogCommand("pagephotos_image_description"));

            // CROP
            editor.addCommand("CropImage", {
                canUndo: false,
                modes: {wysiwyg: 1},
                exec: function(editor) {
                    var selection = editor.getSelection(),
                        element = selection.getStartElement(),
                        image_id = parseInt(element.data('id')) || 0;

                    if (!image_id) {
                        alert(lang.badImage);
                        return
                    }

                    CropDialog(editor.element.$, {
                        buttonSelector: '',

                        beforeOpen: function() {
                            this.id = $(element.$).data('id');
                        },
                        getImage: function() {
                            var source = $(element.$).data('source');
                            if (!source) {
                                // fallback
                                source = $(element.$).attr('src');
                                source = source.replace(/([^\.]+)\.[^\.]+(\.\w+)$/, '$1$2');
                            }
                            return source;
                        },
                        getMinSize: function() {
                            return editor.config.PAGEPHOTOS_MIN_DIMENSIONS;
                        },
                        getMaxSize: function() {
                            return editor.config.PAGEPHOTOS_MAX_DIMENSIONS;
                        },
                        getAspects: function() {
                            return editor.config.PAGEPHOTOS_ASPECTS;
                        },
                        getCropCoords: function() {
                            return this.formatCoords($(element.$).data('crop'));
                        },

                        onCrop: function($button, coords) {
                            $.ajax({
                                url: editor.config.PAGEPHOTOS_CROP_URL,
                                data: {
                                    id: this.id,
                                    croparea: coords.join(':')
                                },
                                dataType: 'json',
                                success: function(response) {
                                    var new_tag = CKEDITOR.dom.element.createFromHtml(response.tag, editor.document);
                                    new_tag.insertAfter(element);
                                    element.remove();

                                    var selection = editor.getSelection();
                                    if (selection.getSelectedElement().$ == new_tag.$) {
                                        var range = selection.getRanges()[0];
                                        var newRange = new CKEDITOR.dom.range(range.document);
                                        newRange.moveToPosition(new_tag, CKEDITOR.POSITION_AFTER_END);
                                        newRange.select();
                                    }
                                }
                            });

                            element.setAttribute('data-crop', coords.join(':'));
                        }
                    }).eventHandler();
                }
            });

            // ROTATE
            var rotate = function(direction) {
                return function(editor) {
                    var selection = editor.getSelection(),
                        element = selection.getStartElement(),
                        image_id = parseInt(element.data('id')) || 0;

                    if (!image_id) {
                        alert(lang.badImage);
                        return
                    }

                    $.ajax({
                        url: editor.config.PAGEPHOTOS_ROTATE_URL,
                        data: {
                            id: image_id,
                            direction: direction
                        },
                        dataType: 'json',
                        success: function(response) {
                            var new_tag = CKEDITOR.dom.element.createFromHtml(response.tag, editor.document);
                            new_tag.insertAfter(element);
                            element.remove();

                            var selection = editor.getSelection();
                            if (selection.getSelectedElement().$ == new_tag.$) {
                                var range = selection.getRanges()[0];
                                var newRange = new CKEDITOR.dom.range(range.document);
                                newRange.moveToPosition(new_tag, CKEDITOR.POSITION_AFTER_END);
                                newRange.select();
                            }
                        }
                    });
                }
            };

            editor.addCommand("RotateCW", {
                canUndo: false,
                modes: {wysiwyg: 1},
                exec: rotate('right')
            });

            editor.addCommand("RotateCCW", {
                canUndo: false,
                modes: {wysiwyg: 1},
                exec: rotate('left')
            });

            // ======================================
            //      CONTEXT MENU
            // ======================================

            // Добавление пунктов в контекстное меню
            editor.addMenuGroup('images');
            editor.addMenuItems({
                _crop_command : {
                    label : lang.contextMenuCrop,
                    icon: this.path + 'crop.png',
                    command : 'CropImage',
                    group : 'images',
                    order: 1
                },
                _rotate_left: {
                    label: lang.contextMenuRotateCW,
                    icon: this.path + 'rotate-cw.png',
                    command: 'RotateCW',
                    group: 'images',
                    order: 2
                },
                _rotate_right: {
                    label: lang.contextMenuRotateCCW,
                    icon: this.path + 'rotate-ccw.png',
                    command: 'RotateCCW',
                    group: 'images',
                    order: 3
                },
                _photos_image_description: {
                    label: lang.contextMenuImageDescr,
                    icon: this.path + 'descr.png',
                    command: 'pagephotos_image_description',
                    group: 'images',
                    order: 4
                },
                _photos_block_description : {
                    label : lang.contextMenuBlockDescr,
                    icon: this.path + 'descr.png',
                    command : 'pagephotos_block_description',
                    group : 'images',
                    order: 5
                }
            });
            editor.contextMenu.addListener(function (element) {
                if (element) {
                    var isImage = element.is('img') && !element.isReadOnly(),
                        isGallery = element.hasClass('page-images'),
                        isInGallery = element.getParent().hasClass('page-images');

                    if (isImage && isInGallery) {
                        return {
                            _crop_command : CKEDITOR.TRISTATE_OFF,
                            _rotate_left : CKEDITOR.TRISTATE_OFF,
                            _rotate_right : CKEDITOR.TRISTATE_OFF,
                            _photos_block_description : CKEDITOR.TRISTATE_OFF,
                            _photos_image_description : CKEDITOR.TRISTATE_OFF
                        }
                    } else if (isGallery) {
                        return {
                            _photos_block_description : CKEDITOR.TRISTATE_OFF
                        }
                    }
                }

                return null
            });


            editor.on('contentDom', function () {
                // Обновление класса галереи при удалении картинок через Backspace и Delete
                editor.on('key', function (evt) {
                    if ((evt.data.keyCode === 8) || (evt.data.keyCode === 46)) {
                        if (editor.mode != "wysiwyg") {
                            return
                        }

                        // if we call getStartElement too soon, we get the wrong element
                        setTimeout(function () {
                            var container = editor.getSelection().getStartElement();
                            if (container.hasClass('page-images')) {
                                if (container.getElementsByTag('img').count() > 1) {
                                    container.removeClass('single-image').addClass('multi-image');
                                } else if (container.getElementsByTag('img').count() == 1) {
                                    container.removeClass('multi-image').addClass('single-image');
                                } else {
                                    container.remove()
                                }
                            }
                        }, 10)
                    }
                })
            });
        }
    })

})();
