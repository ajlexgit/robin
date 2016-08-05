(function() {

    CKEDITOR.dialog.add("imageAttrsDialog", function(editor) {
        return {
            title: 'Alter image attributes',
            minWidth: 400,
            minHeight: 150,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [
                    {
                        id: 'alt',
                        type: 'text',
                        label: 'Alt',
                        setup: function(element) {
                            this.setValue(element.getAttribute("alt"));
                        },
                        commit: function(element) {
                            var alt = this.getValue();
                            if (alt) {
                                element.setAttribute('alt', alt);
                            } else {
                                element.removeAttribute('alt');
                            }
                        }
                    },
                    {
                        id: 'title',
                        type: 'text',
                        label: 'Title',
                        setup: function(element) {
                            this.setValue(element.getAttribute("title"));
                        },
                        commit: function(element) {
                            var title = this.getValue();
                            if (title) {
                                element.setAttribute('title', title);
                            } else {
                                element.removeAttribute('title');
                            }
                        }
                    }
                ]
            }],
            onShow: function() {
                this.element = editor.getSelection().getStartElement();
                this.setupContent(this.element);
            },
            onOk: function() {
                if (this.element) {
                    this.commitContent(this.element);
                }
            }
        }
    });

})();
