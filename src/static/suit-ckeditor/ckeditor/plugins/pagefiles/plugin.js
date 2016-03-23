(function() {

    // Показ окна изменения файла в модальном окне
    var showChangePopup = function (editor, wnd, page_file_id) {
        var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
        var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;
        var w = 800,
            h = 600,
            left = dualScreenLeft + Math.round(window.outerWidth/2 - w/2),
            top = dualScreenTop + Math.round(window.outerHeight/2 - h/2);

        var win = wnd.open(
            editor.config.PAGEFILES_EDIT_URL.replace('1', page_file_id) + '?_popup=1',
            'page_file',
            'height=' + h + ',width=' + w + ',top=' + top + ',left=' + left + ',resizable=yes,scrollbars=yes'
        );
        win.focus();
        return false
    };


    CKEDITOR.plugins.add("pagefiles", {
        icons: 'pagefiles',
        init: function (editor) {
            editor.ui.addButton("PageFiles", {
                label: gettext('Upload files'),
                command: "pagefiles",
                toolbar: 'insert'
            });

            // ======================================
            //      DIALOGS
            // ======================================

            CKEDITOR.dialog.add("pagefiles", this.path + "dialogs/dlg_upload.js");
            CKEDITOR.dialog.add("pagefiles_file_name", this.path + "dialogs/file_name.js");

            // ======================================
            //      COMMANDS
            // ======================================

            // UPLOAD
            editor.addCommand("pagefiles", new CKEDITOR.dialogCommand("pagefiles", {
                allowedContent: 'ul(!page-files)[!data-id]',
                modes: {
                    wysiwyg: 1,
                    source: 0
                },
                canUndo: true
            }));

            // SET Name
            editor.addCommand("pagefiles_file_name", new CKEDITOR.dialogCommand("pagefiles_file_name"));


            // ======================================
            //      CONTEXT MENU
            // ======================================

            // Добавление пунктов в контекстное меню
            editor.addMenuGroup('files');
            editor.addMenuItems({
                _file_name: {
                    label: gettext('Edit name'),
                    icon: this.path + 'edit.png',
                    command: 'pagefiles_file_name',
                    group: 'files',
                    order: 1
                }
            });
            editor.contextMenu.addListener(function (element) {
                if (element) {
                    var ascendant = element.getAscendant('ul');
                    var inFiles = ascendant && ascendant.hasClass('page-files');
                    var isFile = inFiles && (element.is('li') || element.is('a'));
                    if (isFile) {
                        return {
                            _file_name : CKEDITOR.TRISTATE_OFF
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

                        var container = editor.getSelection().getStartElement();
                        if (container.hasClass('page-files')) {
                            // UL
                            container.remove();
                            return
                        }

                        var ascendant = container.getAscendant('ul');
                        var inFiles = ascendant && ascendant.hasClass('page-files');
                        if (inFiles) {
                            evt.cancel();
                            evt.stop();
                        }
                    }
                }, editor, null, 8);
            });
        }
    })

})();
