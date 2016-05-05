(function() {

    CKEDITOR.dialog.add('file_widget_dlg', function(editor) {
        var lang = editor.lang.file_widget;
        return {
            title: lang.dialogTitle,
            minWidth: 320,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'name',
                    type: 'text',
                    required: true,
                    style: 'width:100%',
                    label: 'Name',
                    setup: function(widget) {
                        var text = widget.wrapper.findOne('span');
                        if (text) {
                            this.setValue(text.getText());
                            this.focus(true);
                        }
                    },
                    commit: function(widget) {
                        var text = widget.wrapper.findOne('span');
                        if (text) {
                            text.setText(this.getValue());
                        }
                    }
                }]
            }],
            onShow: function() {
                var selection = editor.getSelection();
                var element = selection.getStartElement();
                var widget = editor.widgets.getByElement(element);

                this.widget = widget;
                this.setupContent(widget);
            },
            onOk: function() {
                this.commitContent(this.widget);
            }
        };
    });

})();