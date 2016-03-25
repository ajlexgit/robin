(function() {

    CKEDITOR.plugins.add("pagefiles", {
        requires: 'file_widget',
        icons: 'pagefiles',
        lang: 'en,ru',
        init: function(editor) {
            var lang = editor.lang.pagefiles;

            editor.ui.addButton("PageFiles", {
                label: lang.buttonTitle,
                command: "pagefiles",
                toolbar: 'insert'
            });

            CKEDITOR.dialog.add("pagefiles", this.path + "dialogs/dlg_upload.js");
            editor.addCommand("pagefiles", new CKEDITOR.dialogCommand("pagefiles", {
                allowedContent: 'div(*); div(!page-file)[!data-id]; span',
                modes: {
                    wysiwyg: 1,
                    source: 0
                },
                canUndo: true
            }));
            editor.addContentsCss(this.path + 'styles/editor.css');

            editor.on('key', function(evt) {
                if ((evt.data.keyCode === 8) || (evt.data.keyCode === 46)) {
                    if (editor.mode != "wysiwyg") {
                        return
                    }

                    // if we call getStartElement too soon, we get the wrong element
                    setTimeout(function() {
                        var containers = editor.document.find('.page-files');
                        for (var i = 0, container; container = containers.getItem(i); i++) {
                            if (!container.getChildCount()) {
                                container.remove();
                            }
                        }
                    }, 10)
                }
            }, null, null, 8);
        }
    })

})();
