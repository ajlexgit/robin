(function() {

    // Показ окна изменения изображения в модальном окне
    var showChangePopup = function (editor, wnd, page_photo_id) {
        var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
        var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;
        var w = 800,
            h = 600,
            left = dualScreenLeft + Math.round(window.outerWidth/2 - w/2),
            top = dualScreenTop + Math.round(window.outerHeight/2 - h/2);

        var win = wnd.open(
            editor.config.PAGEPHOTOS_EDIT_URL.replace('1', page_photo_id) + '?_popup=1',
            'page_photo',
            'height=' + h + ',width=' + w + ',top=' + top + ',left=' + left + ',resizable=yes,scrollbars=yes'
        );
        win.focus();
        return false
    };


    CKEDITOR.plugins.add("pagephotos", {
        icons: 'pagephotos',
        init: function (editor) {
            editor.ui.addButton("PagePhotos", {
                label: gettext('Upload images'),
                command: "pagephotos",
                toolbar: 'insert'
            });

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
                allowedContent: 'p(!page-images,single-image,multi-image); ' +
                                'img(*)[!src,alt,width,height,title,data-id]',
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

            // EDIT
            editor.addCommand("ChangeImage", {
                canUndo: false,
                modes: { wysiwyg:1 },
                exec: function (editor) {
                    var element = editor.getSelection().getStartElement(),
                        image_id = parseInt(element.data('id')) || 0;

                    if (!image_id) {
                        alert(gettext('Impossible to crop the picture.\nPlease contact your system administrator'));
                        return
                    }

                    showChangePopup(editor, editor.window.$, image_id)
                }
            });


            // ======================================
            //      CONTEXT MENU
            // ======================================

            // Добавление пунктов в контекстное меню
            editor.addMenuGroup('images');
            editor.addMenuItems({
                _crop_command : {
                    label : gettext('Edit'),
                    icon: this.path + 'edit.png',
                    command : 'ChangeImage',
                    group : 'images',
                    order : 1
                },
                _block_description : {
                    label : gettext('Block description'),
                    icon: this.path + 'descr.png',
                    command : 'pagephotos_block_description',
                    group : 'images',
                    order : 2
                },
                _image_description : {
                    label : gettext('Image description'),
                    icon: this.path + 'descr.png',
                    command : 'pagephotos_image_description',
                    group : 'images',
                    order : 3
                }
            });
            editor.contextMenu.addListener(function (element) {
                if (element) {
                    var isImage = element.is('img') && !element.isReadOnly(),
                        isGallery = element.hasClass('page-images'),
                        isInGallery = element.getParent().hasClass('page-images');

                    if (isImage && isInGallery) {
                        return {
                            '_crop_command' : CKEDITOR.TRISTATE_OFF,
                            '_block_description' : CKEDITOR.TRISTATE_OFF,
                            '_image_description' : CKEDITOR.TRISTATE_OFF
                        }
                    } else if (isGallery) {
                        return {
                            '_block_description' : CKEDITOR.TRISTATE_OFF
                        }
                    }
                }

                return null
            });


            editor.on('contentDom', function () {
                // Обновление тега изображения при изменении
                editor.window.$.dismissPhotoChangePopup = function(win, newTag, newId) {
                    var element = editor.document.$.querySelector('img[data-id="' + newId + '"]');
                    if (element) {
                        element.outerHTML = newTag.trim();
                    }
                    win.close();
                };

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
