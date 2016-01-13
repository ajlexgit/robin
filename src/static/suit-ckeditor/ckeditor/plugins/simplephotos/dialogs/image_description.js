(function() {

    CKEDITOR.dialog.add("simplephotos_image_description", function (editor) {
		return {
            title: gettext('Set image description'),
            minWidth: 400,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'description',
                    type: 'html',
                    html: '<div>' +
                        '<p>Description (maximum length 128 characters):</p>' +
                        '<textarea ' +
                        'style="width: 100%; height: 4.8em; resize: none; border: 1px solid gray;' +
                        'padding: 5px 8px; font-size: 14px; ' +
                        '-webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;">' +
                        '</textarea>' +
                    '</div>'
                }]
            }],

            onShow: function() {
                var element = editor.getSelection().getStartElement();

                var dialogElement = this.getContentElement('tab-basic', 'description').getElement();
                var textarea = dialogElement.getElementsByTag('textarea').getItem(0);

                textarea.setValue(element.getAttribute('alt'));
                textarea.focus(true);
            },

            onOk: function() {
                var element = editor.getSelection().getStartElement();

                var dialogElement = this.getContentElement('tab-basic', 'description').getElement();
                var textarea = dialogElement.getElementsByTag('textarea').getItem(0);

                element.setAttribute('alt', textarea.getValue());
            }
        }
	})

})();
