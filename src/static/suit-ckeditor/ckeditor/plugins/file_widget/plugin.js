(function() {

    CKEDITOR.plugins.add("file_widget", {
        requires: 'widget',
        icons: 'file_widget',
        init: function(editor) {
            editor.widgets.add('file_widget', {
                upcast: function(element) {
                    return element.hasClass('page-file')
                }
            });

            CKEDITOR.dialog.add('file_widget_dlg', this.path + 'dialogs/file_widget.js');
            editor.addCommand("file_widget_edit", new CKEDITOR.dialogCommand("file_widget_dlg"));

            editor.addMenuGroup('files');
            editor.addMenuItems({
                _edit_files: {
                    label: gettext('Edit Files Box'),
                    icon: this.path + 'edit.png',
                    command: 'file_widget_edit',
                    group: 'files',
                    order: 1
                }
            });
            editor.contextMenu.addListener(function(element) {
                if (element) {
                    if (element.hasAttribute('data-cke-widget-id')) {
                        window.el = element;
                        var wrapper = element.findOne('.page-file');
                        if (wrapper) {
                            return {
                                _edit_files: CKEDITOR.TRISTATE_OFF
                            }
                        }
                    }
                }

                return null
            });
        }
    })

})();
