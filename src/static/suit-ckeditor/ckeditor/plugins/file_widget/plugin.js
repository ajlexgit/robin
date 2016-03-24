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
                if (element && element.hasAttribute('data-cke-widget-id') && element.findOne('.page-file')) {
                    return {
                        _edit_files: CKEDITOR.TRISTATE_OFF
                    }
                }

                return null
            });

            editor.on('drop', function(evt) {
                setTimeout(function() {
                    var target = evt.data.target;
                    var element = evt.data.dropRange.getNextEditableNode();
                    if (element && (element.type == CKEDITOR.NODE_ELEMENT) &&
                        element.hasAttribute('data-cke-widget-id') && element.findOne('.page-file')) {
                        if (target && !target.hasClass('page-files')) {
                            var wrapper = new CKEDITOR.dom.element('div', editor.document);
                            wrapper.addClass('page-files');
                            element.insertBeforeMe(wrapper);
                            wrapper.append(element);
                        }
                    }
                }, 10);
            });

            editor.on('key', function(evt) {
                if ((evt.data.keyCode === 8) || (evt.data.keyCode === 46)) {
                    if (editor.mode != "wysiwyg") {
                        return
                    }

                    var element = editor.getSelection().getStartElement();
                    if (element.hasAttribute('data-cke-widget-id') && element.findOne('.page-file')) {
                        element.remove();
                        evt.stop();
                    }
                }
            });
        }
    })

})();
