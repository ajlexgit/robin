(function() {

    CKEDITOR.plugins.add("columns", {
        requires: 'widget',
        icons: 'columns',
        init: function (editor) {
            editor.addContentsCss(this.path + 'styles/widget.css');

            // ======================================
            //      Widget
            // ======================================
            editor.widgets.add('columns', {
                button: 'Two columns',
                template: '<div class="columns">' +
                '<div class="column column-left"></div>' +
                '<div class="column column-right"></div>' +
                '</div>',
                editables: {
                    left: {
                        selector: '.column-left'
                    },
                    right: {
                        selector: '.column-right'
                    }
                }
            });
        }
    })

})();
