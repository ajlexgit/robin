(function() {

    CKEDITOR.dialog.add("image_description", function (editor) {
		return {
            title: gettext('Set image description'),
            minWidth: 400,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    type: 'html',
                    html: '<p>Description (maximum length 128 characters):</p>'
                },
                {
                    id: 'description',
                    type: 'html',
                    html: '<textarea maxlength="128" ' +
                    'style="width: 100%; height: 4.8em; resize: none; border: 1px solid gray;' +
                    'padding: 5px 8px; font-size: 14px; ' +
                    '-webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;">' +
                    '</textarea>'
                }]
            }],

            onShow: function() {
                var element = editor.getSelection().getStartElement();
                var textarea = this.getContentElement('tab-basic', 'description').getInputElement();
                textarea.setValue(element.getAttribute('alt'));
            },

            onOk: function() {
                var element = editor.getSelection().getStartElement();
                var textarea = this.getContentElement('tab-basic', 'description').getInputElement();
                element.setAttribute('alt', textarea.getValue());
            }
        }
	})

})();
