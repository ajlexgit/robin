(function() {

    CKEDITOR.dialog.add("pagephotos_image_description", function (editor) {
        var lang = editor.lang.pagephotos;
        return {
            title: lang.dialogImageDescr,
            minWidth: 400,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'description',
                    type: 'textarea',
                    label: lang.dialogImageDescrTextarea
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
