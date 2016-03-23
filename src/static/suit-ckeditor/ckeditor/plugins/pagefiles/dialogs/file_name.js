(function() {

    CKEDITOR.dialog.add("pagefiles_file_name", function (editor) {
        return {
            title: gettext('Set file name'),
            minWidth: 400,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'name',
                    type: 'html',
                    html: '<div>' +
                        '<p>Name</p>' +
                        '<input type="text" ' +
                            'style="width: 100%; height: auto; border: 1px solid gray;' +
                            'padding: 5px 8px; font-size: 14px; ' +
                            '-webkit-box-sizing: border-box; ' +
                            '-moz-box-sizing: border-box; box-sizing: border-box;">' +
                    '</div>'
                }]
            }],

            onShow: function() {
                var element = editor.getSelection().getStartElement();

                var dialogElement = this.getContentElement('tab-basic', 'name').getElement();
                var input = dialogElement.getElementsByTag('input').getItem(0);

                input.setValue(element.getText());
                input.focus(true);
            },

            onOk: function() {
                var element = editor.getSelection().getStartElement();

                var dialogElement = this.getContentElement('tab-basic', 'name').getElement();
                var input = dialogElement.getElementsByTag('input').getItem(0);

                var value = input.getValue().trim();
                if (!value) {
                    alert('Name required');
                    return false
                }

                element.setText(value);
            }
        }
    })

})();
