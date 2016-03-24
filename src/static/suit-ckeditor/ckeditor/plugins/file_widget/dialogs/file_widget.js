(function() {

    CKEDITOR.dialog.add('file_widget_dlg', function(editor) {
        return {
            title: 'Edit Files Box',
            minWidth: 200,
            minHeight: 100,
            contents: [{
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [{
                    id: 'name',
                    type: 'html',
                    html: '<div></div>'
                }]
            }]
        };
    });

})();