(function() {

    CKEDITOR.dialog.add('file_widget_dlg', function(editor) {
        return {
            title: 'Edit File Name',
            minWidth: 320,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'name',
                    type: 'html',
                    html: '<div>' +
                        '<p>Enter new name:</p>' +
                        '<input type="text" ' +
                        'style="width: 100%; height: auto; border: 1px solid gray;' +
                        'padding: 5px 8px; font-size: 14px; margin-top: 4px;' +
                        '-webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;">' +
                    '</div>'
                }]
            }],

            onShow: function() {
                var dialogElement = this.getContentElement('tab-basic', 'name').getElement();
                var input = dialogElement.getElementsByTag('input').getItem(0);

                var element = editor.getSelection().getStartElement();
                var link = element.findOne('.page-file a');
                if (link) {
                    input.setValue(link.getText());
                    input.focus(true);
                }
            },

            onOk: function() {
                var dialogElement = this.getContentElement('tab-basic', 'name').getElement();
                var input = dialogElement.getElementsByTag('input').getItem(0);

                var value = input.getValue().trim();
                if (!value) {
                    alert('Name required');
                    return false
                }

                var element = editor.getSelection().getStartElement();
                var link = element.findOne('.page-file a');
                if (link) {
                    link.setText(value);
                }
            }
        };
    });

})();