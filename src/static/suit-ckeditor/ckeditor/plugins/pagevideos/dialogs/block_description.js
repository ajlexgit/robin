(function() {

    var clean_element = function(element) {
        var i = 0;
        var child;
        var childs = element.childNodes;
        while (child = childs[i]) {
            if (child.nodeType != 1) {
                element.removeChild(child);
            } else if (child.tagName != 'IFRAME') {
                element.removeChild(child);
            } else {
                i++
            }
        }
    };

    CKEDITOR.dialog.add("pagevideos_block_description", function (editor) {
		return {
            title: gettext('Set block description'),
            minWidth: 400,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'description',
                    type: 'html',
                    html: '<div>' +
                        '<p>Description:</p>' +
                        '<textarea ' +
                        'style="width: 100%; height: 7em; resize: none; border: 1px solid gray;' +
                        'padding: 5px 8px; font-size: 14px; ' +
                        '-webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;">' +
                        '</textarea>' +
                    '</div>'
                }]
            }],

            onShow: function() {
                var element = editor.getSelection().getStartElement();
                var container = element.hasClass('page-video') ? element : element.getParent();

                var dialogElement = this.getContentElement('tab-basic', 'description').getElement();
                var textarea = dialogElement.getElementsByTag('textarea').getItem(0);

                var description = CKEDITOR.tools.trim(container.$.innerText);
                textarea.setValue( description );
                textarea.focus(true);
            },

            onOk: function() {
                var element = editor.getSelection().getStartElement();
                var container = element.hasClass('page-video') ? element : element.getParent();

                var dialogElement = this.getContentElement('tab-basic', 'description').getElement();
                var textarea = dialogElement.getElementsByTag('textarea').getItem(0);

                clean_element(container.$);

                var description = CKEDITOR.tools.trim(textarea.getValue());
                if (description) {
                    description = description.replace(/\n/g, '<br/>');
                    container.appendHtml('<br/> ' + description);
                }
            }
        }
	})

})();
