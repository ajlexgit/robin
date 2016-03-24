(function() {

    CKEDITOR.plugins.add("pagefiles", {
        requires: 'file_widget',
        icons: 'pagefiles',
        init: function (editor) {
            editor.ui.addButton("PageFiles", {
                label: gettext('Upload files'),
                command: "pagefiles",
                toolbar: 'insert'
            });

            CKEDITOR.dialog.add("pagefiles", this.path + "dialogs/dlg_upload.js");
            editor.addCommand("pagefiles", new CKEDITOR.dialogCommand("pagefiles", {
                allowedContent: 'div(*); div(!page-file)[!data-id]',
                modes: {
                    wysiwyg: 1,
                    source: 0
                },
                canUndo: true
            }));
        }
    })

})();
