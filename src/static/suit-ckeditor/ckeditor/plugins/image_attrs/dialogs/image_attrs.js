(function() {

    CKEDITOR.dialog.add("imageAttrsDialog", function(editor) {
        return {
            title: 'Alter image attributes',
            minWidth: 400,
            minHeight: 150,
            resizable: false,
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
                    },
                    {
                        id: 'description',
                        type: 'textarea',
                        label: 'Description',
                        setup: function(element) {
                            var description = element.getAttribute("data-description");
                            if (description) {
                                this.setValue(atob(description));
                            }
                        },
                        commit: function(element) {
                            var description = this.getValue();
                            if (description) {
                                element.setAttribute('data-description', btoa(description));
                            } else {
                                element.removeAttribute('data-description');
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
