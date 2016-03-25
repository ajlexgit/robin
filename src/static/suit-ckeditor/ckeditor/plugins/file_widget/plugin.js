(function() {

    CKEDITOR.plugins.add("file_widget", {
        requires: 'widget,dialog',
        icons: 'file_widget',
        lang: 'en,ru',
        init: function(editor) {
            var lang = editor.lang.file_widget;

            editor.widgets.add('file_widget', {
                dialog: 'file_widget_dlg',
                upcast: function(element) {
                    return element.hasClass('page-file')
                }
            });

            CKEDITOR.dialog.add('file_widget_dlg', this.path + 'dialogs/file_widget.js');
            editor.addCommand("file_widget_edit", new CKEDITOR.dialogCommand("file_widget_dlg"));
            editor.addContentsCss(this.path + 'styles/editor.css');

            editor.addMenuGroup('files');
            editor.addMenuItems({
                _edit_files: {
                    label: lang.contextMenuEdit,
                    icon: this.path + 'edit.png',
                    command: 'file_widget_edit',
                    group: 'files',
                    order: 1
                }
            });
            editor.contextMenu.addListener(function(element) {
                if (element && element.hasAttribute('data-cke-widget-id') && element.findOne('.page-file')) {
                    return {
                        _edit_files: CKEDITOR.TRISTATE_OFF
                    }
                }

                return null
            });

            editor.on('dragend', function(evt) {
                setTimeout(function() {
                    var widget = evt.editor.widgets.selected[0];
                    if (!widget || (widget.wrapper.type != CKEDITOR.NODE_ELEMENT)) {
                        return
                    }

                    widget = widget.wrapper;
                    if (widget.hasAttribute('data-cke-widget-id') && widget.findOne('.page-file')) {
                        var target = widget.getParent();
                        if (target && !target.hasClass('page-files')) {
                            var wrapper = new CKEDITOR.dom.element('div', editor.document);
                            wrapper.addClass('page-files');
                            widget.insertBeforeMe(wrapper);
                            wrapper.append(widget);
                        }
                    }
                }, 20);
            });
        }
    })

})();
