(function() {

    CKEDITOR.plugins.add("pagevideos", {
        icons: 'pagevideos',
        init: function (editor) {
            editor.ui.addButton("PageVideos", {
                label: gettext('Insert video'),
                command: "pagevideos",
                toolbar: 'insert'
            });

            CKEDITOR.scriptLoader.load(
                CKEDITOR.getUrl(this.path + 'libs/jquery.oembed.js')
            );

            // ======================================
            //      DIALOGS
            // ======================================

            CKEDITOR.dialog.add("pagevideos", this.path + "dialogs/dlg_upload.js");
            CKEDITOR.dialog.add("pagevideos_block_description", this.path + "dialogs/block_description.js");


            // ======================================
            //      COMMANDS
            // ======================================

            // UPLOAD
            editor.addCommand("pagevideos", new CKEDITOR.dialogCommand("pagevideos", {
                allowedContent: 'p(!page-video);' +
                                'p[!data-url];p iframe[*]',
                modes: {
                    wysiwyg: 1,
                    source: 0
                },
                canUndo: true
            }));

            // BLOCK DESCRIPTION
            editor.addCommand("pagevideos_block_description", new CKEDITOR.dialogCommand("pagevideos_block_description"));

            // CHANGE VIDEO
            editor.addCommand("ChangeVideo", {
                exec: function (editor) {
                    editor.openDialog('pagevideos')
                },
                canUndo: false
            });


            // ======================================
            //      CONTEXT MENU
            // ======================================

            // Добавление пунктов в контекстное меню
            editor.addMenuGroup('videos');
            editor.addMenuItems({
                _change_video : {
                    label : gettext('Edit'),
                    icon: this.path + 'edit.png',
                    command : 'ChangeVideo',
                    group : 'videos'
                },
                _block_description : {
                    label : gettext('Block description'),
                    icon: this.path + 'descr.png',
                    command : 'pagevideos_block_description',
                    group : 'videos'
                }
            });
            editor.contextMenu.addListener(function (element) {
                if (element && element.hasClass('page-video')) {
                    return {
                        _change_video : CKEDITOR.TRISTATE_OFF,
                        _block_description : CKEDITOR.TRISTATE_OFF
                    }
                }

                return null
            });


            editor.on('contentDom', function () {
                // Удаление контейнера при удалении видео через Backspace и Delete
                editor.on('key', function (evt) {
                    if ((evt.data.keyCode === 8) || (evt.data.keyCode === 46)) {
                        if (editor.mode != "wysiwyg") {
                            return
                        }

                        // if we call getStartElement too soon, we get the wrong element
                        setTimeout(function () {
                            var container = editor.getSelection().getStartElement();
                            if (container.hasClass('page-video')) {
                                if (container.getElementsByTag('iframe').count() == 0) {
                                    container.remove()
                                }
                            }
                        }, 10)
                    }
                })
            })
        }
    })

})();
