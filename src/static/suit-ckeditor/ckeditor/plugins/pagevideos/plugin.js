(function() {

    CKEDITOR.config.pagevideos = {
        classname: 'page-video'
    };


    CKEDITOR.plugins.add("pagevideos", {
        init: function (editor) {
            var c = editor.addCommand("pagevideos", new CKEDITOR.dialogCommand("pagevideos", {
                allowedContent: 'p(!' + CKEDITOR.config.pagevideos.classname +
                                ');p[!data-url];p iframe[*]'
            }));
            c.modes = {
                wysiwyg: 1,
                source: 0
            };
            c.canUndo = true;

            editor.ui.addButton("PageVideos", {
                label: gettext('Insert video'),
                command: "pagevideos",
                toolbar: 'insert',
                icon: this.path + "oembed.png"
            });

            CKEDITOR.dialog.add("pagevideos", this.path + "dialogs/dlg_upload.js")

            CKEDITOR.scriptLoader.load(
                CKEDITOR.getUrl(this.path + 'libs/jquery.oembed.min.js')
            );


            // Добавление пунктов в контекстное меню
            editor.addMenuGroup('videos');
            editor.addMenuItems({
                '_add_video_description' : {
                    label : gettext('Add description'),
                    icon: this.path + 'descr.png',
                    command : 'AddVideoDescription',
                    group : 'videos',
                    order : 1
                }
            });
            editor.addCommand("AddVideoDescription", {
                canUndo: false,
                modes: { wysiwyg:1 },
                exec: function (editor) {
                    var element = editor.getSelection().getStartElement(),
                        container = element.hasClass(CKEDITOR.config.pagevideos.classname) ? element : element.getParent(),
                        newRange = editor.createRange();

                    // Chrome вставляет ZWS после каждой картинки :(
                    var html = container.getHtml().replace(/\u200B/g, '');
                    html = html.replace(/(&nbsp;|<br>|\s)+$/gi, '');
                    container.setHtml(html);

                    if (container.getText() == '') {
                        container.appendHtml('<br>&nbsp;');
                        newRange.setStart(container, container.getChildCount()-1);
                        newRange.setEndAt(container, CKEDITOR.POSITION_BEFORE_END)
                    } else {
                        newRange.setStartAfter(container.getElementsByTag('br').getItem(0));
                        newRange.setEndAt(container, CKEDITOR.POSITION_BEFORE_END)
                    }

                    editor.getSelection().selectRanges( [ newRange ] )
                }
            });

            editor.addMenuItems({
                '_change_video' : {
                    label : gettext('Edit'),
                    icon: this.path + 'edit.png',
                    command : 'ChangeVideo',
                    group : 'videos',
                    order : 0
                }
            });
            editor.addCommand("ChangeVideo", {
                canUndo: false,
                modes: { wysiwyg:1 },
                exec: function () {
                    CKEDITOR.currentInstance.openDialog('pagevideos')
                }
            });

            editor.contextMenu.addListener(function (element) {
                if (element) {
                    if (element.hasClass(CKEDITOR.config.pagevideos.classname)) {
                        return {
                            '_change_video' : CKEDITOR.TRISTATE_OFF,
                            '_add_video_description' : CKEDITOR.TRISTATE_OFF
                        }
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
                            if (container.hasClass(CKEDITOR.config.pagevideos.classname)) {
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
